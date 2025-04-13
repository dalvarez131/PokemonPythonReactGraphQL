import { gql } from '@apollo/client';

export const GET_POKEMONS = gql`
  query GetPokemons($page: Int!, $perPage: Int!) {
    pokemonsPage(page: $page, perPage: $perPage) {
      items {
        id
        name
        imageUrl
        types {
          name
        }
      }
      pageInfo {
        total
        lastPage
      }
    }
  }
`;

export const GET_POKEMONS_WITH_PAGINATION = gql`
  query GetPokemonsWithPagination($page: Int!, $perPage: Int!) {
    pokemonsPage(page: $page, perPage: $perPage) {
      items {
        id
        name
        height
        weight
        imageUrl
        types {
          id
          name
        }
      }
      pageInfo {
        total
        perPage
        currentPage
        lastPage
        hasNextPage
        hasPreviousPage
      }
    }
  }
`;

export const GET_POKEMON_BY_ID = gql`
  query GetPokemonById($pokemonId: Int!) {
    pokemonById(pokemonId: $pokemonId) {
      id
      name
      height
      weight
      imageUrl
      types {
        id
        name
      }
      abilities
      cries
    }
  }
`;

export const GET_POKEMON_BY_NAME = gql`
  query GetPokemonByName($pokemonName: String!) {
    pokemonByName(pokemonName: $pokemonName) {
      id
      name
      height
      weight
      imageUrl
      types {
        id
        name
      }
      abilities
      cries
    }
  }
`;

export const GET_POKEMON_DETAILS = gql`
  query GetPokemonDetails($id: Int!) {
    pokemon(id: $id) {
      id
      name
      types
      height
      weight
      abilities
      imageUrl
      cryUrl
    }
  }
`;

export const GET_POKEMON_DETAIL = gql`
  query GetPokemonDetail($pokemonId: Int!) {
    pokemonById(pokemonId: $pokemonId) {
      id
      name
      imageUrl
      height
      weight
      types {
        name
      }
      abilities
      cries
    }
  }
`;