import requests
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

# Use absolute imports
from app.models.pokemon import Pokemon, Type
from app.database import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./pokemon.db")
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# PokeAPI URL
POKE_API_URL = "https://pokeapi.co/api/v2/"


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_type(session: AsyncSession, type_name: str) -> Type:
    result = await session.execute(select(Type).where(Type.name == type_name))
    type_obj = result.scalars().first()
    
    if not type_obj:
        type_obj = Type(name=type_name)
        session.add(type_obj)
        await session.commit()
        
    return type_obj


async def populate_pokemon(limit: int = 50):
    await init_db()
    
    # Fetch Pokemon list
    response = requests.get(f"{POKE_API_URL}pokemon?limit={limit}")
    pokemon_list = response.json()["results"]
    
    async with async_session() as session:
        for pokemon_entry in pokemon_list:
            pokemon_url = pokemon_entry["url"]
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
                type_obj = await get_or_create_type(session, type_name)
                pokemon.types.append(type_obj)
            
            await session.commit()
            print(f"Added Pokemon: {pokemon.name}")


if __name__ == "__main__":
    asyncio.run(populate_pokemon()) 