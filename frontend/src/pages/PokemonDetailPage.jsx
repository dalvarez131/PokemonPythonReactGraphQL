import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@apollo/client';
import { GET_POKEMON_BY_ID } from '../utils/queries';
import usePokemonStore from '../stores/pokemonStore';

const PokemonDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const pokemonId = parseInt(id);
  
  const selectedPokemon = usePokemonStore((state) => state.selectedPokemon);
  const setSelectedPokemon = usePokemonStore((state) => state.setSelectedPokemon);
  
  const { loading, error, data } = useQuery(GET_POKEMON_BY_ID, {
    variables: { pokemonId },
    skip: !!selectedPokemon && selectedPokemon.id === pokemonId,
  });
  
  useEffect(() => {
    // If we have data from the query, update the selected Pokemon in the store
    if (data && data.pokemonById) {
      setSelectedPokemon(data.pokemonById);
    }
  }, [data, setSelectedPokemon]);
  
  const handleBack = () => {
    navigate('/');
  };
  
  // Determine which pokemon data to use: from the store or from the query
  const pokemon = selectedPokemon?.id === pokemonId ? selectedPokemon : data?.pokemonById;
  
  if (loading) return <div className="loading">Loading Pokémon details...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;
  if (!pokemon) return <div className="error">Pokémon not found</div>;

  return (
    <div className="container">
      <button className="back-button" onClick={handleBack}>
        &larr; Back to List
      </button>
      
      <div className="pokemon-detail">
        <img 
          src={pokemon.imageUrl} 
          alt={pokemon.name} 
          className="pokemon-detail-image"
        />
        
        <div className="pokemon-detail-info">
          <h1 className="pokemon-detail-name">{pokemon.name}</h1>
          
          <div className="pokemon-types" style={{ justifyContent: 'center' }}>
            {pokemon.types.map((type) => (
              <span 
                key={type.id} 
                className={`pokemon-type type-${type.name}`}
                style={{ fontSize: '14px', padding: '8px 15px' }}
              >
                {type.name}
              </span>
            ))}
          </div>
          
          <div className="pokemon-detail-stats">
            <div className="pokemon-stat">
              <span className="pokemon-stat-label">Height</span>
              <span>{pokemon.height} cm</span>
            </div>
            
            <div className="pokemon-stat">
              <span className="pokemon-stat-label">Weight</span>
              <span>{pokemon.weight} g</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PokemonDetailPage; 