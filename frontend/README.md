# Pokémon GraphQL Frontend

React frontend for the Pokémon web application that consumes a GraphQL API.

## Features

- React with Vite for fast development
- GraphQL integration with Apollo Client
- State management with Zustand
- Responsive design with CSS
- Testing with Jest and Playwright

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
Create a `.env` file with:
```
VITE_API_URL=http://localhost:8000/graphql
```

## Development

Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Testing

Run unit tests:
```bash
npm test
```

Run end-to-end tests (make sure the app is running):
```bash
npm run test:e2e
```

## Building for Production

Build the app for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Deployment

This frontend can be deployed on Vercel or any static site hosting service:

1. Connect your GitHub repository to Vercel
2. Set the environment variables in the Vercel dashboard
3. Deploy

## Project Structure

- `src/components/` - Reusable UI components
- `src/pages/` - Page components for each route
- `src/stores/` - Zustand state management
- `src/utils/` - Utility functions and GraphQL queries
- `tests/` - Jest unit tests
- `playwright/` - Playwright end-to-end tests
