import { useEffect, useState } from 'react'
import './App.css'
import { fetchRecipes, type RecipeSummary } from './api'

function App() {
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
          This React frontend is now connected to your FastAPI backend and is reading
          recipes from the live API.
        </p>
        <div className="hero-actions">
          <a className="primary-link" href="http://127.0.0.1:8000/docs">
            Open API docs
          </a>
          <a className="secondary-link" href="https://react.dev">
            Learn React
          </a>
        </div>
      </section>

      <section className="feature-grid" aria-label="Frontend sections">
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
        <article className="feature-card">
          <h2>Meal plans</h2>
          <p>Create weekly plans from your chosen recipes.</p>
        </article>
        <article className="feature-card">
          <h2>Shopping list</h2>
          <p>Turn planned meals into a consolidated list.</p>
        </article>
      </section>
    </main>
  )
}

export default App
