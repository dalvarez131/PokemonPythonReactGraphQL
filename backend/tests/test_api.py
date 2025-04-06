import pytest
from httpx import AsyncClient
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.models.pokemon import Pokemon, Type


# Setup test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_pokemon.db"
engine = create_async_engine(TEST_DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def setup_database():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Add test data
    async with async_session() as session:
        # Create a type
        fire_type = Type(id=1, name="fire")
        session.add(fire_type)
        
        # Create a Pokemon
        charmander = Pokemon(
            id=4,
            name="charmander",
            height=6,
            weight=85,
            image_url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png"
        )
        charmander.types.append(fire_type)
        session.add(charmander)
        
        await session.commit()
    
    yield
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_pokemons(client, setup_database):
    query = """
    query {
        pokemons {
            id
            name
            height
            weight
            imageUrl
            types {
                name
            }
        }
    }
    """
    
    response = await client.post("/graphql", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert "pokemons" in data["data"]
    pokemons = data["data"]["pokemons"]
    
    assert len(pokemons) > 0
    assert pokemons[0]["name"] == "charmander"
    assert pokemons[0]["types"][0]["name"] == "fire"


@pytest.mark.asyncio
async def test_get_pokemon_by_id(client, setup_database):
    query = """
    query {
        pokemonById(pokemonId: 4) {
            id
            name
            types {
                name
            }
        }
    }
    """
    
    response = await client.post("/graphql", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert "pokemonById" in data["data"]
    pokemon = data["data"]["pokemonById"]
    
    assert pokemon["name"] == "charmander"
    assert pokemon["types"][0]["name"] == "fire"


@pytest.mark.asyncio
async def test_get_pokemon_by_name(client, setup_database):
    query = """
    query {
        pokemonByName(name: "charmander") {
            id
            name
            types {
                name
            }
        }
    }
    """
    
    response = await client.post("/graphql", json={"query": query})
    
    assert response.status_code == 200
    data = response.json()
    
    assert "data" in data
    assert "pokemonByName" in data["data"]
    pokemon = data["data"]["pokemonByName"]
    
    assert pokemon["id"] == 4
    assert pokemon["types"][0]["name"] == "fire" 