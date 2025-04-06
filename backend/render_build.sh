#!/bin/bash
# This script runs during the build phase on Render

# Install dependencies
pip install -r requirements.txt

# Create database and populate with data
cd /opt/render/project/src/
python -c "
import asyncio
import os
import sys
sys.path.insert(0, '.')
from backend.app.models.pokemon import Pokemon, Type
from backend.app.database import Base, engine, async_engine

import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

# Create async session
async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    async with async_engine.begin() as conn:
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

async def populate_pokemon(limit: int = 150):
    await init_db()
    
    # Fetch Pokemon list
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}')
    pokemon_list = response.json()['results']
    
    async with async_session() as session:
        for pokemon_entry in pokemon_list:
            pokemon_url = pokemon_entry['url']
            pokemon_data = requests.get(pokemon_url).json()
            
            # Extract Pokemon details
            pokemon = Pokemon(
                id=pokemon_data['id'],
                name=pokemon_data['name'],
                height=pokemon_data['height'],
                weight=pokemon_data['weight'],
                image_url=pokemon_data['sprites']['other']['official-artwork']['front_default']
            )
            
            session.add(pokemon)
            
            # Add types
            for type_data in pokemon_data['types']:
                type_name = type_data['type']['name']
                type_obj = await get_or_create_type(session, type_name)
                pokemon.types.append(type_obj)
            
            await session.commit()
            print(f'Added Pokemon: {pokemon.name}')

asyncio.run(populate_pokemon())
"

echo "Build completed successfully!" 