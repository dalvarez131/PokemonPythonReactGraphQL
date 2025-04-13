import React from 'react';
import PokemonList from '../components/PokemonList';

const HomePage = () => {
  return (
    <div className="container">
      <h1 style={styles.title}>Explore Pokémon</h1>
      <PokemonList />
    </div>
  );
};

const styles = {
  title: {
    textAlign: 'center',
    margin: '20px 0 30px',
    fontSize: '28px',
  },
};

export default HomePage; 