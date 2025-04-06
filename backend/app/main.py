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

# Set up CORS
origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:5173",  # Vite
    "*",  # Allow all origins for testing
    os.getenv("FRONTEND_URL", ""),  # Deployed frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
            print("No Pokemon found in database. Run the populate_db.py script to populate the database.")
