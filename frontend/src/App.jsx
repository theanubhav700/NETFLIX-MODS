import { useState } from 'react'
import TermsPage     from './pages/TermsPage'
import LandingPage   from './pages/LandingPage'
import CreateAccount from './pages/CreateAccount'
import HomePage      from './pages/HomePage'

const TERMS_KEY = 'nm_terms_accepted'

function getInitialState() {
  // Agar user pehle se logged in hai toh seedha home pe bhejo
  const saved = localStorage.getItem('nm_current_user')
  if (saved) {
    try {
      const user = JSON.parse(saved)
      if (user?.name) return { page: 'home', name: user.name }
    } catch {}
  }
  // Warna terms check karo
  const termsAccepted = localStorage.getItem(TERMS_KEY) === 'yes'
  return { page: termsAccepted ? 'landing' : 'terms', name: '' }
}

function App() {
  const initial = getInitialState()
  const [page, setPage]           = useState(initial.page)
  const [currentUser, setCurrentUser] = useState(initial.name)

  const acceptTerms = () => {
    localStorage.setItem(TERMS_KEY, 'yes')
    setPage('landing')
  }

  const handleCreated = () => {
    const user = JSON.parse(localStorage.getItem('nm_current_user') || '{}')
    setCurrentUser(user.name || 'Friend')
    setPage('home')
  }

  const handleSignIn = (name) => {
    setCurrentUser(name)
    setPage('home')
  }

  const handleLogout = () => {
    localStorage.removeItem('nm_current_user')
    setCurrentUser('')
    setPage('landing')
  }

  if (page === 'terms')  return <TermsPage     onAccept={acceptTerms} />
  if (page === 'create') return <CreateAccount onBack={() => setPage('landing')} onCreated={handleCreated} />
  if (page === 'home')   return <HomePage      name={currentUser} onLogout={handleLogout} />
  return                        <LandingPage   onCreateAccount={() => setPage('create')} onSignIn={handleSignIn} />
}

export default App
