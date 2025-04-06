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
    # Create database tables if they don't exist
    # Note: Production should use migrations
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.future import select
    from sqlalchemy.orm import sessionmaker
    from .models.pokemon import Pokemon
    
    # Ensure we're using the aiosqlite driver explicitly
    db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./pokemon.db")
    if db_url.startswith("sqlite:///"):
        # Convert non-async URL to async URL
        db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    
    engine = create_async_engine(db_url)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Check if there are any Pokemon in the database
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        result = await session.execute(select(Pokemon))
        if not result.scalars().first():
            print("No Pokemon found in database. Populating database with Pokemon data...")
            # Populate the database with Pokemon data
            import requests
            from .models.pokemon import Type
            
            # Populate with initial Pokemon
            pokemon_limit = 50  # You can adjust this number as needed
            
            # Fetch Pokemon list from PokeAPI
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={pokemon_limit}")
            pokemon_list = response.json()["results"]
            
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
                        type_result = await session.execute(select(Type).where(Type.name == type_name))
                        type_obj = type_result.scalars().first()
                        
                        if not type_obj:
                            type_obj = Type(name=type_name)
                            session.add(type_obj)
                            await session.flush()
                        
                        pokemon.types.append(type_obj)
                    
                    await session.commit()
                    print(f"Added Pokemon: {pokemon.name} (ID: {pokemon.id})")
                    
                except Exception as e:
                    print(f"Error adding Pokemon {pokemon_entry['name']}: {e}")
                    await session.rollback()
            
            print("Finished populating database!")
        else:
            print("Database already has Pokemon data.")
