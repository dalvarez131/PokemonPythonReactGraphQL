from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pokemon.db")

# Convert SQLite URL to async URL if needed
ASYNC_DATABASE_URL = DATABASE_URL
if DATABASE_URL.startswith("sqlite:///"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Synchronous engine and session (for scripts and sync operations)
connect_args = {}
if DATABASE_URL.startswith("sqlite:"):
    connect_args = {"check_same_thread": False}
    
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine and session (for FastAPI)
async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base for models
Base = declarative_base()

# Dependency for FastAPI (sync)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for FastAPI (async)
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
