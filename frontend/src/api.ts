export interface RecipeSummary {
  id: number
  name: string
  servings: number
  instructions?: string | null
  source?: string | null
  source_url?: string | null
  ingredients: Array<{
    ingredient_name: string
    ingredient_id?: number | null
    amount: number
    unit: string
  }>
}

export async function fetchRecipes(): Promise<RecipeSummary[]> {
  const response = await fetch('/api/recipes/', { headers: { Accept: 'application/json' } })

  if (!response.ok) {
    throw new Error(`Failed to load recipes (${response.status})`)
  }

  return response.json()
}
