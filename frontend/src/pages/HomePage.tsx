import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import '../App.css'
import { fetchRecipes, type RecipeSummary } from '../api'

function HomePage() {
  const [recipes, setRecipes] = useState<RecipeSummary[]>([])
  const [status, setStatus] = useState<'loading' | 'ready' | 'error'>('loading')
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    async function loadRecipes() {
      try {
        const data = await fetchRecipes()
        setRecipes(data)
        setStatus('ready')
      } catch (error) {
        setStatus('error')
        setErrorMessage(error instanceof Error ? error.message : 'Unknown error')
      }
    }

    void loadRecipes()
  }, [])

  return (
    <main className="app-shell">
      <section className="hero-card">
        <p className="eyebrow">Meal Planner</p>
        <h1>Plan meals, build a shopping list, and stay organized.</h1>
        <p className="hero-text">
          Browse your current recipes and add new ones from their own page.
        </p>
        <div className="hero-actions">
          <Link className="primary-link" to="/recipes/new">
            Create new recipe
          </Link>
          <a className="secondary-link" href="http://127.0.0.1:8000/docs">
            Open API docs
          </a>
        </div>
      </section>

      <section className="feature-grid" aria-label="Recipe overview">
        <article className="feature-card">
          <h2>Recipes</h2>
          {status === 'loading' && <p>Loading recipes…</p>}
          {status === 'error' && <p className="error-text">{errorMessage}</p>}
          {status === 'ready' && recipes.length === 0 && <p>No recipes found yet.</p>}
          {status === 'ready' && recipes.length > 0 && (
            <ul className="recipe-list">
              {recipes.map((recipe) => (
                <li key={recipe.id}>
                  <strong>{recipe.name}</strong>
                  <span>{recipe.servings} servings</span>
                </li>
              ))}
            </ul>
          )}
        </article>
      </section>
    </main>
  )
}

export default HomePage
