import typing
import strawberry
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import get_db, SessionLocal
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


async def get_pokemons(db: AsyncSession):
    result = await db.execute(
        select(Pokemon).options(selectinload(Pokemon.types))
    )
    return result.scalars().all()


async def get_pokemon_by_id(db: AsyncSession, pokemon_id: int):
    result = await db.execute(
        select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.id == pokemon_id)
    )
    return result.scalars().first()


async def get_pokemon_by_name(db: AsyncSession, name: str):
    result = await db.execute(
        select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.name == name)
    )
    return result.scalars().first()


def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@strawberry.type
class Query:
    @strawberry.field
    def pokemons(self) -> typing.List[PokemonType]:
        db = get_db_session()
        result = db.query(Pokemon).options(selectinload(Pokemon.types)).all()
        return result

    @strawberry.field
    def pokemon_by_id(self, pokemon_id: int) -> typing.Optional[PokemonType]:
        db = get_db_session()
        result = db.query(Pokemon).options(selectinload(Pokemon.types)).filter(Pokemon.id == pokemon_id).first()
        return result

    @strawberry.field
    def pokemon_by_name(self, name: str) -> typing.Optional[PokemonType]:
        db = get_db_session()
        result = db.query(Pokemon).options(selectinload(Pokemon.types)).filter(Pokemon.name == name).first()
        return result


schema = strawberry.Schema(Query)
