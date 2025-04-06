import typing
import strawberry
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import AsyncSessionLocal
from .models.pokemon import Pokemon, Type


@strawberry.type
class TypeType:
    id: int
    name: str


@strawberry.type
class PokemonType:
    id: int
    name: str
    height: int
    weight: int
    image_url: str
    types: typing.List[TypeType]


async def get_pokemons():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Pokemon).options(selectinload(Pokemon.types))
        )
        return result.scalars().all()


async def get_pokemon_by_id(pokemon_id: int):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.id == pokemon_id)
        )
        return result.scalars().first()


async def get_pokemon_by_name(name: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.name == name)
        )
        return result.scalars().first()


@strawberry.type
class Query:
    @strawberry.field
    async def pokemons(self) -> typing.List[PokemonType]:
        return await get_pokemons()

    @strawberry.field
    async def pokemon_by_id(self, pokemon_id: int) -> typing.Optional[PokemonType]:
        return await get_pokemon_by_id(pokemon_id)

    @strawberry.field
    async def pokemon_by_name(self, name: str) -> typing.Optional[PokemonType]:
        return await get_pokemon_by_name(name)


schema = strawberry.Schema(Query)
