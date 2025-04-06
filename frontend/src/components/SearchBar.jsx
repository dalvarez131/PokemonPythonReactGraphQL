import React from 'react';
import usePokemonStore from '../stores/pokemonStore';

const SearchBar = () => {
  const searchTerm = usePokemonStore((state) => state.searchTerm);
  const setSearchTerm = usePokemonStore((state) => state.setSearchTerm);

  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleClear = () => {
    setSearchTerm('');
  };

  return (
    <div className="search-container" style={searchStyles.container}>
      <input
        type="text"
        placeholder="Search Pokémon..."
        value={searchTerm}
        onChange={handleChange}
        style={searchStyles.input}
      />
      {searchTerm && (
        <button 
          onClick={handleClear}
          style={searchStyles.clearButton}
        >
          ✕
        </button>
      )}
    </div>
  );
};

const searchStyles = {
  container: {
    position: 'relative',
    maxWidth: '500px',
    margin: '0 auto 30px',
  },
  input: {
    width: '100%',
    padding: '12px 20px',
    fontSize: '16px',
    borderRadius: '30px',
    border: '2px solid #ddd',
    outline: 'none',
    transition: 'border 0.3s',
  },
  clearButton: {
    position: 'absolute',
    right: '15px',
    top: '50%',
    transform: 'translateY(-50%)',
    background: 'none',
    border: 'none',
    fontSize: '16px',
    cursor: 'pointer',
    color: '#999',
  },
};

export default SearchBar; 