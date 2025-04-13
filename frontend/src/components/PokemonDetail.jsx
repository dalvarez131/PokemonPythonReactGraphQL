import React from 'react';
import '../styles/PokemonDetail.css';

const PokemonDetail = ({ pokemon }) => {
  console.log('Pokemon in detail:', pokemon);
  console.log('Abilities:', pokemon.abilities);

  const hasAbilities = Array.isArray(pokemon.abilities) && pokemon.abilities.length > 0;

  return (
    <div className="pokemon-detail">
      <div className="pokemon-detail-header">
        <h2 className="pokemon-detail-name">{pokemon.name}</h2>
        <div className="pokemon-detail-types">
          {pokemon.types.map((type, index) => (
            <span key={index} className={`type-badge type-${type.name}`}>
              {type.name}
            </span>
          ))}
        </div>
      </div>

      <div className="pokemon-detail-content">
        <div className="pokemon-detail-image">
          <img src={pokemon.imageUrl} alt={pokemon.name} />
        </div>

        <div className="pokemon-detail-info">
          <div className="pokemon-detail-stats">
            <div className="stat">
              <span className="stat-label">Height:</span>
              <span className="stat-value">{pokemon.height / 10}m</span>
            </div>
            <div className="stat">
              <span className="stat-label">Weight:</span>
              <span className="stat-value">{pokemon.weight / 10}kg</span>
            </div>
          </div>

          <div className="pokemon-detail-abilities">
            <h3>Abilities</h3>
            <div className="abilities-list">
              {hasAbilities ? (
                pokemon.abilities.map((ability, index) => (
                  <span key={index} className="ability-badge">
                    {ability}
                  </span>
                ))
              ) : (
                <span className="ability-badge">Loading abilities...</span>
              )}
            </div>
          </div>

          {pokemon.cries && (
            <div className="pokemon-detail-cry">
              <h3>Cry</h3>
              <audio controls>
                <source src={pokemon.cries} type="audio/ogg" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PokemonDetail;