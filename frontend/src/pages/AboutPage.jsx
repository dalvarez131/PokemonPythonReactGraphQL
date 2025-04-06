import React from 'react';

const AboutPage = () => {
  return (
    <div className="container">
      <div style={styles.aboutContainer}>
        <h1 style={styles.title}>About This App</h1>
        
        <div style={styles.card}>
          <h2 style={styles.subtitle}>Pokémon GraphQL Explorer</h2>
          <p style={styles.text}>
            This application demonstrates the integration of FastAPI with GraphQL on the backend
            and React with Apollo Client on the frontend.
          </p>
          
          <h3 style={styles.featureTitle}>Features:</h3>
          <ul style={styles.list}>
            <li>FastAPI backend with GraphQL (Strawberry)</li>
            <li>SQLite database for storing Pokémon data</li>
            <li>React frontend with Apollo Client for GraphQL queries</li>
            <li>Pokémon data sourced from the PokéAPI</li>
            <li>Search functionality for finding Pokémon</li>
            <li>Responsive design for all devices</li>
            <li>State management with Zustand</li>
          </ul>
          
          <h3 style={styles.featureTitle}>Technology Stack:</h3>
          <ul style={styles.list}>
            <li><strong>Backend:</strong> Python, FastAPI, GraphQL, SQLAlchemy</li>
            <li><strong>Frontend:</strong> React, Apollo Client, Zustand</li>
            <li><strong>Testing:</strong> Pytest (backend), Jest and Playwright (frontend)</li>
            <li><strong>Deployment:</strong> Railway (backend), Vercel (frontend)</li>
          </ul>
        </div>
        
        <p style={styles.footer}>
          Created as a demonstration project. Pokémon data and images are provided by the&nbsp;
          <a href="https://pokeapi.co/" target="_blank" rel="noopener noreferrer" style={styles.link}>
            PokéAPI
          </a>.
        </p>
      </div>
    </div>
  );
};

const styles = {
  aboutContainer: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
  },
  title: {
    textAlign: 'center',
    marginBottom: '30px',
    fontSize: '28px',
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '25px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '30px',
  },
  subtitle: {
    fontSize: '22px',
    marginBottom: '15px',
    color: '#ff0000',
  },
  text: {
    lineHeight: '1.6',
    marginBottom: '20px',
  },
  featureTitle: {
    fontSize: '18px',
    marginBottom: '10px',
    marginTop: '20px',
  },
  list: {
    paddingLeft: '20px',
    marginBottom: '20px',
  },
  footer: {
    textAlign: 'center',
    fontSize: '14px',
    color: '#666',
  },
  link: {
    color: '#ff0000',
    textDecoration: 'none',
  },
};

export default AboutPage; 