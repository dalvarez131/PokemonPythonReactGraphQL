import { create } from 'zustand';

const usePokemonStore = create((set) => ({
  selectedPokemon: null,
  searchTerm: '',
  
  setSelectedPokemon: (pokemon) => set({ selectedPokemon: pokemon }),
  clearSelectedPokemon: () => set({ selectedPokemon: null }),
  
  setSearchTerm: (term) => set({ searchTerm: term }),
  clearSearchTerm: () => set({ searchTerm: '' }),
}));

export default usePokemonStore; 