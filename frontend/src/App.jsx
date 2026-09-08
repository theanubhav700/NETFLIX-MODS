import { useState } from 'react'
import TermsPage      from './pages/TermsPage'
import LandingPage    from './pages/LandingPage'
import CreateAccount  from './pages/CreateAccount'

const TERMS_KEY = 'nm_terms_accepted'

function App() {
  // If user already accepted terms before, start directly on landing
  const [page, setPage] = useState(
    () => localStorage.getItem(TERMS_KEY) === 'yes' ? 'landing' : 'terms'
  )

  const acceptTerms = () => {
    localStorage.setItem(TERMS_KEY, 'yes')
    setPage('landing')
  }

  if (page === 'terms')   return <TermsPage     onAccept={acceptTerms} />
  if (page === 'create')  return <CreateAccount onBack={() => setPage('landing')} />
  return                         <LandingPage   onCreateAccount={() => setPage('create')} />
}

export default App
