from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from ..database import Base

# Association table for many-to-many relationship between Pokemon and Types
pokemon_type = Table(
    'pokemon_type', 
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemons.id')),
    Column('type_id', Integer, ForeignKey('types.id'))
)

class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    image_url = Column(String)
    
    # Relationship with Type model through association table
    types = relationship("Type", secondary=pokemon_type, back_populates="pokemons")

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationship with Pokemon model through association table
    pokemons = relationship("Pokemon", secondary=pokemon_type, back_populates="types")
