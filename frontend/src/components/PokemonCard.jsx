import React from 'react';
import { useNavigate } from 'react-router-dom';
import usePokemonStore from '../stores/pokemonStore';

const PokemonCard = ({ pokemon }) => {
  const navigate = useNavigate();
  const setSelectedPokemon = usePokemonStore((state) => state.setSelectedPokemon);

  const handleClick = () => {
    setSelectedPokemon(pokemon);
    navigate(`/pokemon/${pokemon.id}`);
  };

  return (
    <div className="pokemon-card" onClick={handleClick}>
      <img 
        src={pokemon.imageUrl} 
        alt={pokemon.name} 
        className="pokemon-card-image"
      />
      <div className="pokemon-card-content">
        <h3 className="pokemon-card-name">{pokemon.name}</h3>
        <div className="pokemon-types">
          {pokemon.types.map((type) => (
            <span 
              key={type.id} 
              className={`pokemon-type type-${type.name}`}
            >
              {type.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PokemonCard; 