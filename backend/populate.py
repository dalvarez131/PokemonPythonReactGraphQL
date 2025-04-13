from app.populate_db import populate_pokemon
import asyncio

if __name__ == "__main__":
    asyncio.run(populate_pokemon()) 