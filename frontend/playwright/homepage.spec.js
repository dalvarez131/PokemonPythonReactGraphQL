// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test.beforeEach(async ({ page }) => {
    // Mock the GraphQL response for Pokemon list
    await page.route('**/graphql', async route => {
      const json = route.request().postDataJSON();
      
      if (json.query.includes('GetPokemons')) {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              pokemons: [
                {
                  id: 1,
                  name: 'bulbasaur',
                  imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png',
                  types: [{ id: 1, name: 'grass' }, { id: 2, name: 'poison' }]
                },
                {
                  id: 4,
                  name: 'charmander',
                  imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png',
                  types: [{ id: 3, name: 'fire' }]
                }
              ]
            }
          })
        });
      } else {
        return route.continue();
      }
    });
    
    await page.goto('http://localhost:3000');
  });

  test('should display the header with title', async ({ page }) => {
    await expect(page.locator('.logo')).toHaveText('Pokémon GraphQL');
  });

  test('should display Pokemon cards', async ({ page }) => {
    // Wait for Pokemon cards to be visible
    await page.waitForSelector('.pokemon-card');
    
    // Check if we have two Pokemon cards
    const pokemonCards = page.locator('.pokemon-card');
    await expect(pokemonCards).toHaveCount(2);
    
    // Check if the Pokemon names are displayed correctly
    const firstPokemonName = pokemonCards.nth(0).locator('.pokemon-card-name');
    await expect(firstPokemonName).toHaveText('bulbasaur');
    
    const secondPokemonName = pokemonCards.nth(1).locator('.pokemon-card-name');
    await expect(secondPokemonName).toHaveText('charmander');
  });

  test('should filter Pokemon with search bar', async ({ page }) => {
    // Type in the search bar
    await page.fill('input[placeholder="Search Pokémon..."]', 'char');
    
    // Wait for the filtered list
    await page.waitForTimeout(300); // Small delay for the search to process
    
    // Check if only the matching Pokemon is displayed
    const pokemonCards = page.locator('.pokemon-card');
    await expect(pokemonCards).toHaveCount(1);
    await expect(pokemonCards.locator('.pokemon-card-name')).toHaveText('charmander');
    
    // Clear the search
    await page.click('button');
    
    // Check if all Pokemon are displayed again
    await expect(pokemonCards).toHaveCount(2);
  });

  test('should navigate to Pokemon details on card click', async ({ page }) => {
    // Mock the GraphQL response for Pokemon details
    await page.route('**/graphql', async route => {
      const json = route.request().postDataJSON();
      
      if (json.query.includes('GetPokemonById')) {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            data: {
              pokemonById: {
                id: 1,
                name: 'bulbasaur',
                height: 7,
                weight: 69,
                imageUrl: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png',
                types: [{ id: 1, name: 'grass' }, { id: 2, name: 'poison' }]
              }
            }
          })
        });
      }
    });
    
    // Click on the first Pokemon card
    await page.click('.pokemon-card:first-child');
    
    // Verify we are on the Pokemon detail page
    await expect(page).toHaveURL(/pokemon\/1/);
    await expect(page.locator('.pokemon-detail-name')).toHaveText('bulbasaur');
    
    // Test back button
    await page.click('.back-button');
    await expect(page).toHaveURL('/');
  });
}); 