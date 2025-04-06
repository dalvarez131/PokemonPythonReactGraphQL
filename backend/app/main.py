import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from dotenv import load_dotenv

from .graphql_schema import schema
from .database import Base  # Remove engine from import to avoid conflicts

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Pokemon GraphQL API",
    description="A GraphQL API for Pokemon data",
    version="0.1.0"
)

# Set up CORS - Ensure all origins are allowed including Vercel
origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:5173",  # Vite
    "https://pokemon-python-react-graphql.vercel.app",  # Vercel frontend
    "*",  # Allow all origins for testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Welcome to the Pokemon GraphQL API. Go to /graphql for the GraphQL playground."}

@app.on_event("startup")
async def startup_event():
    # Create database tables if they don't exist and populate if empty
    # Using synchronous approach to avoid greenlet issues
    import threading
    
    def setup_db():
        from sqlalchemy import create_engine, inspect
        from sqlalchemy.orm import sessionmaker
        import requests
        
        # Use synchronous SQLAlchemy to avoid greenlet issues
        from .models.pokemon import Pokemon, Type
        
        # Database setup - Use synchronous SQLAlchemy
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pokemon.db")
        if DATABASE_URL.startswith("sqlite+aiosqlite:"):
            DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite:", "sqlite:")
        
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(engine)
        
        # Check if there are any Pokemon in the database
        session = Session()
        try:
            pokemon_count = session.query(Pokemon).count()
            if pokemon_count == 0:
                print("No Pokemon found in database. Populating database with Pokemon data...")
                
                # Populate with initial Pokemon
                pokemon_limit = 50  # You can adjust this number as needed
                
                # Fetch Pokemon list from PokeAPI
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={pokemon_limit}")
                pokemon_list = response.json()["results"]
                
                print(f"Fetched {len(pokemon_list)} Pokemon. Now adding to database...")
                
                for i, pokemon_entry in enumerate(pokemon_list):
                    print(f"Processing Pokemon {i+1}/{len(pokemon_list)}: {pokemon_entry['name']}")
                    
                    pokemon_url = pokemon_entry["url"]
                    try:
                        pokemon_data = requests.get(pokemon_url).json()
                        
                        # Extract Pokemon details
                        pokemon = Pokemon(
                            id=pokemon_data["id"],
                            name=pokemon_data["name"],
                            height=pokemon_data["height"],
                            weight=pokemon_data["weight"],
                            image_url=pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
                        )
                        
                        session.add(pokemon)
                        
                        # Add types
                        for type_data in pokemon_data["types"]:
                            type_name = type_data["type"]["name"]
                            # Check if type exists
                            type_obj = session.query(Type).filter_by(name=type_name).first()
                            
                            if not type_obj:
                                type_obj = Type(name=type_name)
                                session.add(type_obj)
                                session.flush()
                            
                            pokemon.types.append(type_obj)
                        
                        # Commit after each Pokemon
                        session.commit()
                        print(f"Added Pokemon: {pokemon.name} (ID: {pokemon.id})")
                        
                    except Exception as e:
                        print(f"Error adding Pokemon {pokemon_entry['name']}: {e}")
                        session.rollback()
                
                print("Finished populating database!")
            else:
                print(f"Database already has {pokemon_count} Pokemon.")
        finally:
            session.close()
    
    # Run database setup in a separate thread to not block the main event loop
    db_thread = threading.Thread(target=setup_db)
    db_thread.start()
    
    # Optional: Wait for the thread to complete if you want to ensure DB is ready before serving requests
    # db_thread.join()
