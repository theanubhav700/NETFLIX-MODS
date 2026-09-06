import { useState } from 'react'
import TermsPage from './pages/TermsPage'
import LandingPage from './pages/LandingPage'

function App() {
  const [accepted, setAccepted] = useState(false)

  return accepted
    ? <LandingPage />
    : <TermsPage onAccept={() => setAccepted(true)} />
}

export default App
