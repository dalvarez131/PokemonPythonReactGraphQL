from sqlalchemy import Column, Integer, String, Table, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla de asociación para tipos de Pokémon
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

class Pokemon(Base):
    __tablename__ = "pokemons"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    image_url = Column(String)
    abilities = Column(JSON)
    cries = Column(String)
    
    types = relationship("Type", secondary=pokemon_type, backref="pokemon")
