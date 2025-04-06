# Pokémon GraphQL App

A full-stack web application showcasing Pokémon data using FastAPI, GraphQL, React, and SQLite.

## Features

- **Backend**: FastAPI with GraphQL API (Strawberry)
- **Frontend**: React with Apollo Client and Zustand
- **Database**: SQLite for local development
- **Data Source**: PokéAPI for Pokémon data
- **Testing**: Pytest for backend, Jest and Playwright for frontend
- **Deployment**: Railway for backend, Vercel for frontend

## Project Structure

```
.
├── backend/                # FastAPI + GraphQL backend
│   ├── app/                # Application code
│   │   ├── models/         # SQLAlchemy models
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── graphql_schema.py # Strawberry GraphQL schema
│   │   ├── database.py     # Database connection
│   │   └── populate_db.py  # Script to fetch data from PokéAPI
│   └── tests/              # Backend tests
│
└── frontend/              # React frontend
    ├── src/               # Source code
    │   ├── components/    # Reusable components
    │   ├── pages/         # Page components
    │   ├── stores/        # Zustand stores
    │   └── utils/         # Utilities and GraphQL queries
    ├── tests/             # Jest unit tests
    └── playwright/        # Playwright E2E tests
```

## Setup and Installation

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Populate the database with Pokémon data:
```bash
cd app
python -m populate_db
```

5. Start the FastAPI server:
```bash
cd ..
uvicorn app.main:app --reload
```

The backend API will be available at http://localhost:8000, with the GraphQL playground at http://localhost:8000/graphql.

### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000.

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test           # Run Jest unit tests
npm run test:e2e   # Run Playwright E2E tests
```

## Deployment

### Backend Deployment (Railway)

1. Create a new project in Railway
2. Connect your GitHub repository
3. Set up the environment variables:
   - `DATABASE_URL` (for production database)
   - `FRONTEND_URL` (for CORS)
4. Deploy the backend service

### Frontend Deployment (Vercel)

1. Connect your GitHub repository to Vercel
2. Set the environment variables:
   - `VITE_API_URL` (URL of your deployed backend GraphQL endpoint)
3. Deploy the frontend

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- [PokéAPI](https://pokeapi.co/) - The RESTful Pokémon API
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for Python
- [Strawberry GraphQL](https://strawberry.rocks/) - GraphQL library for Python
- [React](https://reactjs.org/) - JavaScript library for building user interfaces
- [Apollo Client](https://www.apollographql.com/docs/react/) - State management library for GraphQL
- [Zustand](https://github.com/pmndrs/zustand) - State management solution for React
- [Playwright](https://playwright.dev/) - E2E testing library 