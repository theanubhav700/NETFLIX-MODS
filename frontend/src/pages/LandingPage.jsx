import { useState, useEffect } from 'react'
import './LandingPage.css'

const LANGUAGES = ['English', 'हिन्दी']

export default function LandingPage() {
  const [loading, setLoading]     = useState(true)
  const [langOpen, setLangOpen]   = useState(false)
  const [selectedLang, setSelectedLang] = useState('English')

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="landing-root">
      {/* ── Navbar ── */}
      <nav className="landing-nav">
        <div className="landing-logo">
          <span className="brand-logo">NETFLIX MODS</span>
        </div>
        <div className="landing-nav-right">
          <button className="account-request-btn">ACCOUNT REQUEST</button>
          <div className="lang-dropdown-wrapper">
            <button
              className="lang-btn"
              onClick={() => setLangOpen(!langOpen)}
              aria-haspopup="listbox"
              aria-expanded={langOpen}
            >
              <svg className="lang-globe-icon" viewBox="0 0 16 16" fill="currentColor">
                <path d="M8 0a8 8 0 100 16A8 8 0 008 0zm0 1.5a6.5 6.5 0 110 13A6.5 6.5 0 018 1.5zm2.94 3.06c.27.58.47 1.23.58 1.94H10.5a9.2 9.2 0 00-.3-1.2l.74-.74zM8 2.08c.38.5.7 1.16.94 1.92H7.06c.24-.76.56-1.42.94-1.92zm-3.68.98l.74.74c-.14.37-.24.77-.3 1.2H3.48a6.54 6.54 0 011.84-1.94zM3.09 6.5h1.67c-.05.49-.08.99-.08 1.5s.03 1.01.08 1.5H3.09a6.46 6.46 0 010-3zm.39 4.5h1.28c.06.43.16.83.3 1.2l-.74.74A6.54 6.54 0 013.48 11zm2.58 2.92c-.38-.5-.7-1.16-.94-1.92h1.88c-.24.76-.56 1.42-.94 1.92zm.94-3.42H7.06c-.06-.48-.09-.99-.09-1.5s.03-1.02.09-1.5H9.94c.06.48.09.99.09 1.5s-.03 1.02-.09 1.5zM8 13.92c-.38-.5-.7-1.16-.94-1.92h1.88c-.24.76-.56 1.42-.94 1.92zm2.94-.98l-.74-.74c.14-.37.24-.77.3-1.2h1.28a6.54 6.54 0 01-1.84 1.94zm2.21-2.44h-1.67c.05-.49.08-.99.08-1.5s-.03-1.01-.08-1.5h1.67a6.46 6.46 0 010 3zm-.37-4.5h-1.28a7.2 7.2 0 00-.3-1.2l.74-.74a6.54 6.54 0 01.84 1.94zm-2.72-2.92c.38.5.7 1.16.94 1.92H9.06c-.24-.76-.56-1.42-.94-1.92z" />
              </svg>
              <span>{selectedLang}</span>
              <svg className={`lang-chevron ${langOpen ? 'open' : ''}`} viewBox="0 0 10 6" fill="currentColor">
                <path d="M0 0l5 6 5-6z" />
              </svg>
            </button>
            {langOpen && (
              <ul className="lang-dropdown" role="listbox">
                {LANGUAGES.map((lang) => (
                  <li
                    key={lang}
                    role="option"
                    aria-selected={selectedLang === lang}
                    className={`lang-option ${selectedLang === lang ? 'active' : ''}`}
                    onClick={() => { setSelectedLang(lang); setLangOpen(false) }}
                  >
                    {lang}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </nav>

      {/* ── Main ── */}
      <main className="landing-main">
        {loading ? (
          <div className="spinner-wrapper" aria-label="Loading" role="status">
            <div className="spinner" />
          </div>
        ) : (
          <>
            {/* Hero */}
            <section className="hero-content">
              <h1 className="hero-title">Unlimited movies, TV<br />shows, and more</h1>
              <p className="hero-sub">Watch anywhere.</p>
              <p className="hero-cta-text">Ready to watch? Enter your email to create your account.</p>
              <div className="hero-email-row">
                <input type="email" placeholder="Email address" className="hero-email-input" aria-label="Email address" />
                <button className="hero-get-started-btn">Get Started &nbsp;›</button>
              </div>
            </section>


          </>
        )}
      </main>
    </div>
  )
}
