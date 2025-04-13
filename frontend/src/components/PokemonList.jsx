import React, { useState } from 'react';
import { useQuery } from '@apollo/client';
import { GET_POKEMONS, GET_POKEMON_DETAIL } from '../utils/queries';
import PokemonDetail from './PokemonDetail';
import '../styles/PokemonList.css';

const PokemonList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPokemonId, setSelectedPokemonId] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 20;

  const { loading, error, data } = useQuery(GET_POKEMONS, {
    variables: {
      page: currentPage,
      perPage: itemsPerPage
    }
  });

  const { data: pokemonDetailData } = useQuery(GET_POKEMON_DETAIL, {
    variables: { pokemonId: selectedPokemonId },
    skip: !selectedPokemonId,
    onCompleted: (data) => {
      console.log('Pokemon detail data:', data);
    }
  });

  if (loading) return <div className="loading">Loading Pokémon...</div>;
  if (error) return <div className="error">Error loading Pokémon: {error.message}</div>;

  const pokemons = data?.pokemonsPage?.items || [];
  const pageInfo = data?.pokemonsPage?.pageInfo || { total: 0, lastPage: 1 };
  
  const filteredPokemons = pokemons.filter(pokemon =>
    pokemon.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const renderPagination = () => {
    const pages = [];
    const lastPage = pageInfo.lastPage;
    const maxVisiblePages = 5;

    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(lastPage, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    if (startPage > 1) {
      pages.push(
        <button
          key={1}
          className="pagination-button"
          onClick={() => handlePageChange(1)}
        >
          1
        </button>
      );
      if (startPage > 2) {
        pages.push(<span key="start-ellipsis" className="pagination-ellipsis">...</span>);
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(
        <button
          key={i}
          className={`pagination-button ${currentPage === i ? 'active' : ''}`}
          onClick={() => handlePageChange(i)}
        >
          {i}
        </button>
      );
    }

    if (endPage < lastPage) {
      if (endPage < lastPage - 1) {
        pages.push(<span key="end-ellipsis" className="pagination-ellipsis">...</span>);
      }
      pages.push(
        <button
          key={lastPage}
          className="pagination-button"
          onClick={() => handlePageChange(lastPage)}
        >
          {lastPage}
        </button>
      );
    }

    return (
      <div className="pagination">
        <button
          className="pagination-button"
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        {pages}
        <button
          className="pagination-button"
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === lastPage}
        >
          Next
        </button>
      </div>
    );
  };

  return (
    <div className="pokemon-list-container">
      <div className="search-container">
        <input
          type="text"
          placeholder="Search Pokémon..."
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setCurrentPage(1);
          }}
          className="search-input"
        />
      </div>

      <div className="pokemon-grid">
        {filteredPokemons.map((pokemon) => (
          <div
            key={pokemon.id}
            className="pokemon-card"
            onClick={() => setSelectedPokemonId(pokemon.id)}
          >
            <img
              src={pokemon.imageUrl}
              alt={pokemon.name}
              className="pokemon-image"
            />
            <h3 className="pokemon-name">{pokemon.name}</h3>
            <div className="pokemon-types">
              {pokemon.types.map((type, index) => (
                <span key={index} className={`type-badge type-${type.name}`}>
                  {type.name}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {renderPagination()}

      {pokemonDetailData?.pokemonById && (
        <div className="modal-overlay" onClick={() => setSelectedPokemonId(null)}>
          <div onClick={(e) => e.stopPropagation()}>
            <PokemonDetail pokemon={pokemonDetailData.pokemonById} />
          </div>
        </div>
      )}
    </div>
  );
};

export default PokemonList; 