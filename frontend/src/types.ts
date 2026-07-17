export interface RecipePayload {
  name: string
  servings: number
  instructions?: string | null
  source?: string | null
  source_url?: string | null
}

export interface RecipeIngredientPayload {
  amount: number
  unit: string
  ingredient_name?: string | null
  ingredient_id?: number | null
}

export interface Recipe extends RecipePayload {
  id: number
  ingredients: RecipeIngredientPayload[]
}
