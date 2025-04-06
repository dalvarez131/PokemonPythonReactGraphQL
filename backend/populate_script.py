"""
Script to populate the database with Pokemon data.
Run this from the backend directory with: python populate_script.py
"""
import sys
import os
import asyncio

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.populate_db import populate_pokemon

if __name__ == "__main__":
    print("Starting to populate the database with Pokemon data...")
    asyncio.run(populate_pokemon(limit=50))
    print("Database population complete!") 