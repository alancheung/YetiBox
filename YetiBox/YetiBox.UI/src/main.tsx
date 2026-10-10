import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.scss'
import AppComponent from './App.tsx'
import { BrowserRouter } from 'react-router'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <AppComponent />
    </BrowserRouter>
  </StrictMode>,
)
