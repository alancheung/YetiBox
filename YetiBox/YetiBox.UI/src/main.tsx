import './index.scss'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import { YetiBoxRouter } from './Router'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <YetiBoxRouter />
    </BrowserRouter>
  </StrictMode>,
)
