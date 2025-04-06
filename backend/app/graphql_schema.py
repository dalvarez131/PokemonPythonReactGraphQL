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
    image_url: str = strawberry.field(name="imageUrl")
    types: typing.List[TypeType]


@strawberry.type
class Query:
    @strawberry.field
    async def pokemons(
        self, 
        page: int = 1, 
        perPage: int = 15
    ) -> typing.List[PokemonType]:
        # Validate input
        if page < 1:
            page = 1
        if perPage < 1:
            perPage = 15
        if perPage > 100:  # Limit maximum items per page
            perPage = 100
            
        async with AsyncSessionLocal() as db:
            # Get total count
            count_result = await db.execute(select(func.count(Pokemon.id)))
            total = count_result.scalar()
            
            # Calculate pagination values
            pages = (total + perPage - 1) // perPage
            offset = (page - 1) * perPage
            
            # Get paginated results
            result = await db.execute(
                select(Pokemon)
                .options(selectinload(Pokemon.types))
                .order_by(Pokemon.id)
                .offset(offset)
                .limit(perPage)
            )
            return result.scalars().all()

    @strawberry.field
    async def pokemons_page(
        self, 
        page: int = 1, 
        perPage: int = 15
    ) -> "PokemonPage":
        # Validate input
        if page < 1:
            page = 1
        if perPage < 1:
            perPage = 15
        if perPage > 100:  # Limit maximum items per page
            perPage = 100
            
        async with AsyncSessionLocal() as db:
            # Get total count
            count_result = await db.execute(select(func.count(Pokemon.id)))
            total = count_result.scalar()
            
            # Calculate pagination values
            pages = (total + perPage - 1) // perPage
            offset = (page - 1) * perPage
            
            # Get paginated results
            result = await db.execute(
                select(Pokemon)
                .options(selectinload(Pokemon.types))
                .order_by(Pokemon.id)
                .offset(offset)
                .limit(perPage)
            )
            pokemons = result.scalars().all()
            
            # Create response object
            page_info = PageInfo(
                total=total,
                page=page,
                per_page=perPage,
                pages=pages,
                has_next=page < pages,
                has_prev=page > 1
            )
            
            return PokemonPage(
                pokemons=pokemons,
                page_info=page_info
            )

    @strawberry.field
    async def pokemon_by_id(
        self, 
        pokemonId: int = 1
    ) -> typing.Optional[PokemonType]:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.id == pokemonId)
            )
            return result.scalars().first()

    @strawberry.field
    async def pokemon_by_name(self, name: str) -> typing.Optional[PokemonType]:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Pokemon).options(selectinload(Pokemon.types)).where(Pokemon.name == name)
            )
            return result.scalars().first()


@strawberry.type
class PageInfo:
    total: int
    page: int
    per_page: int = strawberry.field(name="perPage")
    pages: int
    has_next: bool = strawberry.field(name="hasNext")
    has_prev: bool = strawberry.field(name="hasPrev")


@strawberry.type
class PokemonPage:
    pokemons: typing.List[PokemonType]
    page_info: PageInfo = strawberry.field(name="pageInfo")


schema = strawberry.Schema(Query)
