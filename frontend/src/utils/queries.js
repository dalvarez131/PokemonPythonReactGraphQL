import { gql } from '@apollo/client';

export const GET_POKEMONS = gql`
  query GetPokemons {
    pokemons {
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