import React from 'react';
import '../styles/PokemonCard.css';

const PokemonCard = ({ pokemon }) => {
  return (
    <div className="pokemon-card">
      <div className="pokemon-image">
        <img src={pokemon.imageUrl} alt={pokemon.name} />
      </div>
      
      <div className="pokemon-info">
        <h2>{pokemon.name}</h2>
        
        <div className="pokemon-types">
          {pokemon.types.map(type => (
            <span key={type.id} className={`type-badge type-${type.name}`}>
              {type.name}
            </span>
          ))}
        </div>
        
        <div className="pokemon-stats">
          <div className="stat">
            <span className="stat-label">Height:</span>
            <span className="stat-value">{pokemon.height / 10}m</span>
          </div>
          <div className="stat">
            <span className="stat-label">Weight:</span>
            <span className="stat-value">{pokemon.weight / 10}kg</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PokemonCard; 