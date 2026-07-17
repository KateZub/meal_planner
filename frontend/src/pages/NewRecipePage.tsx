import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import '../App.css'
import { addRecipeIngredients, createRecipe } from '../api'
import type { RecipeIngredientPayload, RecipePayload } from '../types'

const emptyForm: RecipePayload = {
  name: '',
  servings: 1,
  instructions: '',
  source: '',
  source_url: '',
}

const emptyIngredient: RecipeIngredientPayload = {
  amount: 1,
  unit: 'g',
  ingredient_name: '',
}

function NewRecipePage() {
  const navigate = useNavigate()
  const [form, setForm] = useState<RecipePayload>(emptyForm)
  const [ingredients, setIngredients] = useState<RecipeIngredientPayload[]>([emptyIngredient])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setIsSubmitting(true)
    setErrorMessage('')
    setSuccessMessage('')

    const payload: RecipePayload = {
      ...form,
      name: form.name.trim(),
      instructions: form.instructions?.trim() || null,
      source: form.source?.trim() || null,
      source_url: form.source_url?.trim() || null,
    }

    try {
      const createdRecipe = await createRecipe(payload)

      const validIngredients = ingredients
        .filter((ingredient) => ingredient.ingredient_name?.trim())
        .map((ingredient) => ({
          ...ingredient,
          ingredient_name: ingredient.ingredient_name?.trim(),
          amount: Number(ingredient.amount),
          unit: ingredient.unit,
        }))

      if (validIngredients.length > 0) {
        await addRecipeIngredients(createdRecipe.id, validIngredients)
      }

      setSuccessMessage(`Recipe "${createdRecipe.name}" created.`)
      setForm(emptyForm)
      setIngredients([emptyIngredient])
      navigate('/')
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-card">
        <p className="eyebrow">Meal Planner</p>
        <h1>Create a new recipe</h1>
        <p className="hero-text">
          Add a recipe to your collection and save it through the FastAPI backend.
        </p>
        <div className="hero-actions">
          <Link className="secondary-link" to="/">
            Back to recipes
          </Link>
        </div>
      </section>

      <section className="feature-grid" aria-label="Recipe form">
        <article className="feature-card">
          <form className="recipe-form" onSubmit={handleSubmit}>
            <label>
              Name
              <input
                required
                minLength={3}
                value={form.name}
                onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
              />
            </label>
            <label>
              Servings
              <input
                type="number"
                min="1"
                value={form.servings}
                onChange={(event) =>
                  setForm((current) => ({ ...current, servings: Number(event.target.value) }))
                }
              />
            </label>
            <label>
              Instructions
              <textarea
                rows={5}
                value={form.instructions ?? ''}
                onChange={(event) =>
                  setForm((current) => ({ ...current, instructions: event.target.value }))
                }
              />
            </label>
            <label>
              Source
              <input
                value={form.source ?? ''}
                onChange={(event) =>
                  setForm((current) => ({ ...current, source: event.target.value }))
                }
              />
            </label>
            <label>
              Source URL
              <input
                type="url"
                value={form.source_url ?? ''}
                onChange={(event) =>
                  setForm((current) => ({ ...current, source_url: event.target.value }))
                }
              />
            </label>

            <div className="ingredients-section">
              <div className="ingredients-header">
                <h3>Ingredients</h3>
                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => setIngredients((current) => [...current, { ...emptyIngredient }])}
                >
                  Add ingredient
                </button>
              </div>

              {ingredients.map((ingredient, index) => (
                <div key={`ingredient-row-${index}`} className="ingredient-row">
                  <input
                    placeholder="Ingredient name"
                    value={ingredient.ingredient_name ?? ''}
                    onChange={(event) =>
                      setIngredients((current) =>
                        current.map((item, itemIndex) =>
                          itemIndex === index ? { ...item, ingredient_name: event.target.value } : item,
                        ),
                      )
                    }
                  />
                  <input
                    type="number"
                    min="1"
                    value={ingredient.amount}
                    onChange={(event) =>
                      setIngredients((current) =>
                        current.map((item, itemIndex) =>
                          itemIndex === index ? { ...item, amount: Number(event.target.value) } : item,
                        ),
                      )
                    }
                  />
                  <select
                    value={ingredient.unit}
                    onChange={(event) =>
                      setIngredients((current) =>
                        current.map((item, itemIndex) =>
                          itemIndex === index ? { ...item, unit: event.target.value } : item,
                        ),
                      )
                    }
                  >
                    <option value="g">g</option>
                    <option value="ml">ml</option>
                    <option value="ks">ks</option>
                    <option value="ČL">ČL</option>
                    <option value="PL">PL</option>
                    <option value="špetka">špetka</option>
                  </select>
                  <button
                    type="button"
                    className="link-button"
                    onClick={() =>
                      setIngredients((current) => current.filter((_, itemIndex) => itemIndex !== index))
                    }
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>

            {errorMessage && <p className="error-text">{errorMessage}</p>}
            {successMessage && <p className="success-text">{successMessage}</p>}
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Creating…' : 'Create recipe'}
            </button>
          </form>
        </article>
      </section>
    </main>
  )
}

export default NewRecipePage
