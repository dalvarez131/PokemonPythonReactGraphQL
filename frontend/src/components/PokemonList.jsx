import React from 'react';
import { useQuery } from '@apollo/client';
import { GET_POKEMONS } from '../utils/queries';
import PokemonCard from './PokemonCard';
import usePokemonStore from '../stores/pokemonStore';

const PokemonList = () => {
  const { loading, error, data } = useQuery(GET_POKEMONS);
  const searchTerm = usePokemonStore((state) => state.searchTerm);

  if (loading) return <div className="loading">Loading Pokémon...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;

  const pokemons = data.pokemons;
  
  // Filter pokemons based on search term
  const filteredPokemons = pokemons.filter(pokemon => 
    pokemon.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="pokemon-grid">
      {filteredPokemons.length > 0 ? (
        filteredPokemons.map(pokemon => (
          <PokemonCard key={pokemon.id} pokemon={pokemon} />
        ))
      ) : (
        <div className="error">No Pokémon found matching "{searchTerm}"</div>
      )}
    </div>
  );
};

export default PokemonList; 