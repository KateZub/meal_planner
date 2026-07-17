import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './index.css'
import HomePage from './pages/HomePage.tsx'
import NewRecipePage from './pages/NewRecipePage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/recipes/new" element={<NewRecipePage />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
