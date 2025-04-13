import typing
import strawberry
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func

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
    imageUrl: str
    types: typing.List[TypeType]


@strawberry.type
class PokemonDetailType:
    id: int
    name: str
    height: int
    weight: int
    imageUrl: str
    types: typing.List[TypeType]
    abilities: typing.List[str]
    cries: str


@strawberry.type
class PageInfo:
    total: int
    perPage: int
    currentPage: int
    lastPage: int
    hasNextPage: bool
    hasPreviousPage: bool


@strawberry.type
class PokemonConnection:
    items: typing.List[PokemonType]
    pageInfo: PageInfo


@strawberry.type
class Query:
    @strawberry.field
    async def pokemons(
        self, 
        page: int = 1, 
        perPage: int = 15
    ) -> typing.List[PokemonType]:
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * perPage
            query = select(Pokemon).options(selectinload(Pokemon.types)).offset(offset).limit(perPage)
            result = await session.execute(query)
            pokemons = result.scalars().all()
            
            return [
                PokemonType(
                    id=pokemon.id,
                    name=pokemon.name,
                    height=pokemon.height,
                    weight=pokemon.weight,
                    imageUrl=pokemon.image_url,
                    types=[TypeType(id=t.id, name=t.name) for t in pokemon.types]
                )
                for pokemon in pokemons
            ]

    @strawberry.field
    async def pokemonsPage(
        self, 
        page: int = 1, 
        perPage: int = 15
    ) -> PokemonConnection:
        async with AsyncSessionLocal() as session:
            # Obtener el total de Pokémon
            count_query = select(Pokemon)
            count_result = await session.execute(count_query)
            total = len(count_result.scalars().all())
            
            # Calcular información de paginación
            last_page = (total + perPage - 1) // perPage
            has_next_page = page < last_page
            has_previous_page = page > 1
            
            # Obtener los Pokémon de la página actual
            offset = (page - 1) * perPage
            query = select(Pokemon).options(selectinload(Pokemon.types)).offset(offset).limit(perPage)
            result = await session.execute(query)
            pokemons = result.scalars().all()
            
            return PokemonConnection(
                items=[
                    PokemonType(
                        id=pokemon.id,
                        name=pokemon.name,
                        height=pokemon.height,
                        weight=pokemon.weight,
                        imageUrl=pokemon.image_url,
                        types=[TypeType(id=t.id, name=t.name) for t in pokemon.types]
                    )
                    for pokemon in pokemons
                ],
                pageInfo=PageInfo(
                    total=total,
                    perPage=perPage,
                    currentPage=page,
                    lastPage=last_page,
                    hasNextPage=has_next_page,
                    hasPreviousPage=has_previous_page
                )
            )

    @strawberry.field
    async def pokemonById(
        self, 
        pokemonId: int = 1
    ) -> typing.Optional[PokemonDetailType]:
        async with AsyncSessionLocal() as session:
            query = select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.id == pokemonId)
            result = await session.execute(query)
            pokemon = result.scalar_one_or_none()
            
            if pokemon:
                return PokemonDetailType(
                    id=pokemon.id,
                    name=pokemon.name,
                    height=pokemon.height,
                    weight=pokemon.weight,
                    imageUrl=pokemon.image_url,
                    types=[TypeType(id=t.id, name=t.name) for t in pokemon.types],
                    abilities=pokemon.abilities or [],
                    cries=pokemon.cries or ""
                )
            return None

    @strawberry.field
    async def pokemonByName(
        self, 
        pokemonName: str
    ) -> typing.Optional[PokemonDetailType]:
        async with AsyncSessionLocal() as session:
            query = select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.name == pokemonName)
            result = await session.execute(query)
            pokemon = result.scalar_one_or_none()
            
            if pokemon:
                return PokemonDetailType(
                    id=pokemon.id,
                    name=pokemon.name,
                    height=pokemon.height,
                    weight=pokemon.weight,
                    imageUrl=pokemon.image_url,
                    types=[TypeType(id=t.id, name=t.name) for t in pokemon.types],
                    abilities=pokemon.abilities or [],
                    cries=pokemon.cries or ""
                )
            return None


schema = strawberry.Schema(Query)
