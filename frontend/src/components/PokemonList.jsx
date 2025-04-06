import React, { useState } from 'react';
import { useQuery } from '@apollo/client';
import { GET_POKEMONS } from '../utils/queries';
import PokemonCard from './PokemonCard';
import usePokemonStore from '../stores/pokemonStore';

const PokemonList = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const pokemonsPerPage = 15;
  
  const { loading, error, data } = useQuery(GET_POKEMONS, {
    variables: { page: currentPage, perPage: pokemonsPerPage }
  });
  
  const searchTerm = usePokemonStore((state) => state.searchTerm);

  if (loading) return <div className="loading">Loading Pokémon...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;

  const pokemons = data.pokemons;
  
  // Filter pokemons based on search term
  const filteredPokemons = pokemons.filter(pokemon => 
    pokemon.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Manually calculate pagination info
  const hasNext = pokemons.length === pokemonsPerPage;  // If we got a full page, assume there are more
  const hasPrev = currentPage > 1;

  // Handle page changes
  const handlePrevPage = () => {
    if (hasPrev) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (hasNext) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <div className="pokemon-container">
      <div className="pokemon-grid">
        {filteredPokemons.length > 0 ? (
          filteredPokemons.map(pokemon => (
            <PokemonCard key={pokemon.id} pokemon={pokemon} />
          ))
        ) : (
          <div className="error">No Pokémon found matching "{searchTerm}"</div>
        )}
      </div>
      
      {/* Pagination controls */}
      <div className="pagination">
        <button 
          onClick={handlePrevPage} 
          disabled={!hasPrev}
          className={`pagination-btn ${!hasPrev ? 'disabled' : ''}`}
        >
          Previous
        </button>
        
        <span className="page-info">
          Page {currentPage}
        </span>
        
        <button 
          onClick={handleNextPage} 
          disabled={!hasNext}
          className={`pagination-btn ${!hasNext ? 'disabled' : ''}`}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default PokemonList; 