import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css' // <-- AQUÍ VA LA LÍNEA QUE CARGA TAILWIND

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)