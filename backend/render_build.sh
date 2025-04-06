#!/bin/bash
# This script runs during the build phase on Render

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Create a simple script to populate the database
cat > populate_db.py << 'EOF'
import os
import sys
import requests
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define models directly in this script to avoid import issues
Base = declarative_base()

# Association table for Pokemon and Type (many-to-many)
pokemon_type = Table(
    "pokemon_type",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemon.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("type.id"), primary_key=True),
)

class Type(Base):
    __tablename__ = "type"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    
    def __repr__(self):
        return f"<Type(name='{self.name}')>"

class Pokemon(Base):
    __tablename__ = "pokemon"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    image_url = Column(String)
    
    # Relationship with Type
    types = relationship("Type", secondary=pokemon_type, backref="pokemon")
    
    def __repr__(self):
        return f"<Pokemon(name='{self.name}')>"

# Database setup - Use synchronous SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pokemon.db")
# Ensure we're using a synchronous URL
if DATABASE_URL.startswith("sqlite+aiosqlite:"):
    DATABASE_URL = DATABASE_URL.replace("sqlite+aiosqlite:", "sqlite:")

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    print("Initializing database...")
    # Drop all tables first to ensure a clean database
    Base.metadata.drop_all(engine)
    # Create all tables
    Base.metadata.create_all(engine)
    print("Database initialized.")

def get_or_create_type(session, type_name):
    type_obj = session.query(Type).filter_by(name=type_name).first()
    
    if not type_obj:
        type_obj = Type(name=type_name)
        session.add(type_obj)
        session.commit()
        
    return type_obj

def populate_pokemon(limit=150):
    print(f"Starting to populate with {limit} Pokemon...")
    init_db()
    
    # Fetch Pokemon list from PokeAPI
    print("Fetching Pokemon list from PokeAPI...")
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}")
    pokemon_list = response.json()["results"]
    
    print(f"Fetched {len(pokemon_list)} Pokemon. Now adding to database...")
    
    session = Session()
    try:
        for i, pokemon_entry in enumerate(pokemon_list):
            print(f"Processing Pokemon {i+1}/{len(pokemon_list)}: {pokemon_entry['name']}")
            
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
            
            # Commit after each Pokemon to avoid long transactions
            session.commit()
            print(f"Added Pokemon: {pokemon.name} (ID: {pokemon.id})")
    
        print("Finished populating database!")
    except Exception as e:
        print(f"Error populating database: {e}")
        session.rollback()
        raise
    finally:
        session.close()

# Run the script
if __name__ == "__main__":
    print("Running database population script...")
    populate_pokemon(50)
    print("Script completed successfully!")
EOF

# Run the database population script
echo "Running database population script..."
python populate_db.py

echo "Build completed successfully!" 