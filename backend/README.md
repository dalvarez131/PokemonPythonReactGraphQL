# Pokémon GraphQL API

Backend for the Pokémon web application with FastAPI and GraphQL.

## Features

- FastAPI with GraphQL API using Strawberry
- SQLite database (SQLAlchemy ORM)
- GraphQL queries to fetch Pokémon data
- Type relationships
- Database population script

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
DATABASE_URL=sqlite:///./pokemon.db
```

4. Populate the database with Pokémon data:
```bash
cd app
python -m populate_db
```

## Running the API

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- http://localhost:8000 - API root
- http://localhost:8000/graphql - GraphQL playground

## Testing

Run tests with Pytest:
```bash
pytest
```

## GraphQL Queries

Example queries:

```graphql
# Get all Pokémon
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

# Get Pokémon by ID
query {
  pokemonById(pokemonId: 25) {
    name
    height
    weight
    imageUrl
    types {
      name
    }
  }
}

# Get Pokémon by name
query {
  pokemonByName(name: "pikachu") {
    id
    name
    imageUrl
    types {
      name
    }
  }
}
```