import { gql } from '@apollo/client';

export const GET_POKEMONS = gql`
  query GetPokemons($page: Int!, $perPage: Int!) {
    pokemons(page: $page, perPage: $perPage) {
      id
      name
      imageUrl
      types {
        id
        name
      }
    }
  }
`;

export const GET_POKEMONS_WITH_PAGINATION = gql`
  query GetPokemonsWithPagination($page: Int!, $perPage: Int!) {
    pokemonsPage(page: $page, perPage: $perPage) {
      pokemons {
        id
        name
        imageUrl
        types {
          id
          name
        }
      }
      pageInfo {
        total
        page
        perPage
        pages
        hasNext
        hasPrev
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
    }
  }
`;

export const GET_POKEMON_BY_NAME = gql`
  query GetPokemonByName($name: String!) {
    pokemonByName(name: $name) {
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
  }
`; 