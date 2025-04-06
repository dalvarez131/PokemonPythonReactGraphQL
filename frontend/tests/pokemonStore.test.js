import { beforeEach, describe, expect, it } from '@jest/globals';
import usePokemonStore from '../src/stores/pokemonStore';

describe('Pokemon Store', () => {
  beforeEach(() => {
    // Reset the store before each test
    usePokemonStore.setState({
      selectedPokemon: null,
      searchTerm: '',
    });
  });

  it('should initialize with default values', () => {
    const { selectedPokemon, searchTerm } = usePokemonStore.getState();
    expect(selectedPokemon).toBeNull();
    expect(searchTerm).toBe('');
  });

  it('should set selected Pokemon', () => {
    const pokemon = { id: 1, name: 'bulbasaur' };
    usePokemonStore.getState().setSelectedPokemon(pokemon);
    
    const { selectedPokemon } = usePokemonStore.getState();
    expect(selectedPokemon).toEqual(pokemon);
  });

  it('should clear selected Pokemon', () => {
    // First set a Pokemon
    usePokemonStore.getState().setSelectedPokemon({ id: 1, name: 'bulbasaur' });
    
    // Then clear it
    usePokemonStore.getState().clearSelectedPokemon();
    
    const { selectedPokemon } = usePokemonStore.getState();
    expect(selectedPokemon).toBeNull();
  });

  it('should set search term', () => {
    const term = 'char';
    usePokemonStore.getState().setSearchTerm(term);
    
    const { searchTerm } = usePokemonStore.getState();
    expect(searchTerm).toBe(term);
  });

  it('should clear search term', () => {
    // First set a search term
    usePokemonStore.getState().setSearchTerm('char');
    
    // Then clear it
    usePokemonStore.getState().clearSearchTerm();
    
    const { searchTerm } = usePokemonStore.getState();
    expect(searchTerm).toBe('');
  });
}); 