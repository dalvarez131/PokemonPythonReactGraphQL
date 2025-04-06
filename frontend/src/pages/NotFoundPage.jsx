import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="container" style={styles.container}>
      <h1 style={styles.title}>404 - Page Not Found</h1>
      <p style={styles.text}>
        Oops! It looks like the page you're looking for doesn't exist.
      </p>
      <img 
        src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/54.png" 
        alt="Psyduck confused" 
        style={styles.image} 
      />
      <Link to="/" style={styles.button}>
        Return to Home
      </Link>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '70vh',
    textAlign: 'center',
    padding: '20px',
  },
  title: {
    fontSize: '32px',
    marginBottom: '20px',
    color: '#ff0000',
  },
  text: {
    fontSize: '18px',
    marginBottom: '30px',
    maxWidth: '500px',
  },
  image: {
    width: '200px',
    height: '200px',
    marginBottom: '30px',
  },
  button: {
    backgroundColor: '#ff0000',
    color: 'white',
    padding: '12px 24px',
    borderRadius: '8px',
    textDecoration: 'none',
    fontWeight: 'bold',
    transition: 'background-color 0.3s',
  },
};

export default NotFoundPage; 