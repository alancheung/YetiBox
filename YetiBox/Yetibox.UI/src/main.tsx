import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.scss'
import AppComponent from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppComponent />
  </StrictMode>,
)
