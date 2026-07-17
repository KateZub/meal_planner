import type { Recipe, RecipePayload, RecipeIngredientPayload } from './types'

export type RecipeSummary = Recipe

export async function fetchRecipes(): Promise<RecipeSummary[]> {
  const response = await fetch('/api/recipes/', { headers: { Accept: 'application/json' } })

  if (!response.ok) {
    throw new Error(`Failed to load recipes (${response.status})`)
  }

  return response.json()
}

export async function createRecipe(payload: RecipePayload): Promise<Recipe> {
  const response = await fetch('/api/recipes/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Failed to create recipe (${response.status}): ${errorText}`)
  }

  return response.json()
}

export async function addRecipeIngredients(recipeId: number, ingredients: RecipeIngredientPayload[]): Promise<void> {
  const response = await fetch(`/api/recipes/${recipeId}/ingredients`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(ingredients),
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(`Failed to add ingredients (${response.status}): ${errorText}`)
  }
}
