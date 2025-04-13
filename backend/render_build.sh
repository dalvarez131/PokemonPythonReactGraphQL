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
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define models directly in this script to avoid import issues
Base = declarative_base()

# Association table for Pokemon and Type (many-to-many)
pokemon_type = Table(
    "pokemon_type",
    Base.metadata,
    Column("pokemon_id", Integer, ForeignKey("pokemons.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("type.id"), primary_key=True),
)

class Type(Base):
    __tablename__ = "type"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    
    def __repr__(self):
        return f"<Type(name='{self.name}')>"

class Pokemon(Base):
    __tablename__ = "pokemons"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    image_url = Column(String)
    abilities = Column(JSON)
    cries = Column(String)
    
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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate_database():
    # Eliminar tablas existentes y crear nuevas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    
    try:
        # Obtener los primeros 250 Pokémon
        for pokemon_id in range(1, 251):
            try:
                # Obtener datos del Pokémon
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
                pokemon_data = response.json()
                
                # Obtener el grito más reciente
                cries_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
                cries_data = cries_response.json()
                latest_cry = cries_data.get("cries", {}).get("latest", "")
                
                # Extraer habilidades
                abilities = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
                
                # Crear Pokémon
                pokemon = Pokemon(
                    id=pokemon_id,
                    name=pokemon_data["name"],
                    height=pokemon_data["height"],
                    weight=pokemon_data["weight"],
                    image_url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png",
                    abilities=abilities,
                    cries=latest_cry
                )
                
                # Procesar tipos
                for type_data in pokemon_data["types"]:
                    type_name = type_data["type"]["name"]
                    type_obj = session.query(Type).filter(Type.name == type_name).first()
                    if not type_obj:
                        type_obj = Type(name=type_name)
                        session.add(type_obj)
                    pokemon.types.append(type_obj)
                
                session.add(pokemon)
                session.commit()
                print(f"Pokémon {pokemon_id} ({pokemon.name}) añadido exitosamente")
                
            except Exception as e:
                print(f"Error procesando Pokémon {pokemon_id}: {str(e)}")
                session.rollback()
                continue
    
    except Exception as e:
        print(f"Error general: {str(e)}")
        session.rollback()
    finally:
        session.close()

# Run the script
if __name__ == "__main__":
    print("Iniciando población de la base de datos...")
    populate_database()
    print("Población de la base de datos completada.")
EOF

# Run the database population script
echo "Running database population script..."
python populate_db.py

echo "Build completed successfully!" 