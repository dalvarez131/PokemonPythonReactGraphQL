import React, { useState } from 'react';
import { useQuery } from '@apollo/client';
import { GET_POKEMONS_WITH_PAGINATION } from '../utils/queries';
import PokemonCard from './PokemonCard';
import usePokemonStore from '../stores/pokemonStore';

const PokemonList = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const pokemonsPerPage = 15;
  
  const { loading, error, data } = useQuery(GET_POKEMONS_WITH_PAGINATION, {
    variables: { page: currentPage, perPage: pokemonsPerPage }
  });
  
  const searchTerm = usePokemonStore((state) => state.searchTerm);

  if (loading) return <div className="loading">Loading Pokémon...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;

  const { pokemons, pageInfo } = data.pokemonsPage;
  
  // Filter pokemons based on search term
  const filteredPokemons = pokemons.filter(pokemon => 
    pokemon.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Handle page changes
  const handlePrevPage = () => {
    if (pageInfo.hasPrev) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (pageInfo.hasNext) {
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
          disabled={!pageInfo.hasPrev}
          className={`pagination-btn ${!pageInfo.hasPrev ? 'disabled' : ''}`}
        >
          Previous
        </button>
        
        <span className="page-info">
          Page {pageInfo.page} of {pageInfo.pages} (Total: {pageInfo.total} Pokémon)
        </span>
        
        <button 
          onClick={handleNextPage} 
          disabled={!pageInfo.hasNext}
          className={`pagination-btn ${!pageInfo.hasNext ? 'disabled' : ''}`}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default PokemonList; 