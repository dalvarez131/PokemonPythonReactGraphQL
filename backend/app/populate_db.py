import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Use absolute imports
from app.models.pokemon import Pokemon, Type
from app.database import Base

load_dotenv()

DATABASE_URL = "sqlite:///./pokemon.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# PokeAPI URL
POKE_API_URL = "https://pokeapi.co/api/v2/"

def init_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def get_or_create_type(session, type_name: str) -> Type:
    type_obj = session.query(Type).filter(Type.name == type_name).first()
    
    if not type_obj:
        type_obj = Type(name=type_name)
        session.add(type_obj)
        session.commit()
        
    return type_obj

def populate_pokemon(limit: int = 50):
    init_db()
    
    # Fetch Pokemon list
    response = requests.get(f"{POKE_API_URL}pokemon?limit={limit}")
    pokemon_list = response.json()["results"]
    
    session = Session()
    try:
        for pokemon_entry in pokemon_list:
            pokemon_url = pokemon_entry["url"]
            pokemon_data = requests.get(pokemon_url).json()
            
            # Extract abilities
            abilities = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
            
            # Get cry URL
            cry_url = f"https://play.pokemonshowdown.com/audio/cries/{pokemon_data['name'].lower()}.ogg"
            
            # Extract Pokemon details
            pokemon = Pokemon(
                id=pokemon_data["id"],
                name=pokemon_data["name"],
                height=pokemon_data["height"],
                weight=pokemon_data["weight"],
                image_url=pokemon_data["sprites"]["other"]["official-artwork"]["front_default"],
                abilities=abilities,
                cries=cry_url
            )
            
            session.add(pokemon)
            
            # Add types
            for type_data in pokemon_data["types"]:
                type_name = type_data["type"]["name"]
                type_obj = get_or_create_type(session, type_name)
                pokemon.types.append(type_obj)
            
            session.commit()
            print(f"Added Pokemon: {pokemon.name} with abilities: {abilities}")
    finally:
        session.close()

if __name__ == "__main__":
    populate_pokemon() 