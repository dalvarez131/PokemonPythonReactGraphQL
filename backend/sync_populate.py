"""
A synchronous script to populate the database with Pokemon data.
Run this from the backend directory with: python sync_populate.py
"""
import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the current directory to the Python path
import sys
sys.path.insert(0, os.path.abspath('.'))

from app.models.pokemon import Pokemon, Type, Base

load_dotenv()

# Use SQLite database
DATABASE_URL = "sqlite:///./pokemon.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PokeAPI URL
POKE_API_URL = "https://pokeapi.co/api/v2/"

def get_or_create_type(session, type_name):
    type_obj = session.query(Type).filter(Type.name == type_name).first()
    if not type_obj:
        type_obj = Type(name=type_name)
        session.add(type_obj)
        session.commit()
    return type_obj

def populate_pokemon(limit=50):
    # Create all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Fetch Pokemon list
    response = requests.get(f"{POKE_API_URL}pokemon?limit={limit}")
    pokemon_list = response.json()["results"]
    
    session = SessionLocal()
    try:
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
                type_obj = get_or_create_type(session, type_name)
                pokemon.types.append(type_obj)
            
            session.commit()
            print(f"Added Pokemon: {pokemon.name}")
    finally:
        session.close()

if __name__ == "__main__":
    print("Starting to populate the database with Pokemon data...")
    populate_pokemon(limit=50)
    print("Database population complete!") 