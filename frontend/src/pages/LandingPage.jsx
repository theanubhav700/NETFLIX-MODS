import { useState, useEffect } from 'react'
import './LandingPage.css'

const T = {
  English: {
    brand:          'NETFLIX MODS',
    accountRequest: 'ACCOUNT REQUEST',
    heroTitle:      <>Unlimited movies, TV<br />shows, and more</>,
    heroSub:        'Watch anywhere.',
    heroCta:        'Ready to watch? Sign in or create a new account.',
    emailPlaceholder:    'Email address',
    emailLabel:          'Email address',
    passwordPlaceholder: 'Password',
    passwordLabel:       'Password',
    signIn:         'Sign In',
    newHere:        'New here?',
    createAccount:  'Create an account',
    showPassword:   'Show password',
    hidePassword:   'Hide password',
  },
}

export default function LandingPage({ onCreateAccount }) {
  const [loading, setLoading] = useState(true)
  const [email, setEmail]     = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)

  const txt = T.English

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="landing-root">
      {/* ── Navbar ── */}
      <nav className="landing-nav">
        <div className="landing-logo">
          <span className="brand-logo">{txt.brand}</span>
        </div>
        <div className="landing-nav-right">
          <button className="account-request-btn">{txt.accountRequest}</button>
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
            <section className="hero-content">
              <h1 className="hero-title">{txt.heroTitle}</h1>
              <p className="hero-sub">{txt.heroSub}</p>
              <p className="hero-cta-text">{txt.heroCta}</p>

              {/* Email input */}
              <div className="hero-input-group">
                <span className="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="4" width="20" height="16" rx="2" />
                    <path d="M2 7l10 7 10-7" />
                  </svg>
                </span>
                <input
                  type="email"
                  placeholder={txt.emailPlaceholder}
                  className="hero-icon-input"
                  aria-label={txt.emailLabel}
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                />
              </div>

              {/* Password input */}
              <div className="hero-input-group">
                <span className="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="5" y="11" width="14" height="10" rx="2" />
                    <path d="M8 11V7a4 4 0 018 0v4" />
                    <circle cx="12" cy="16" r="1.2" fill="currentColor" stroke="none" />
                  </svg>
                </span>
                <input
                  type={showPass ? 'text' : 'password'}
                  placeholder={txt.passwordPlaceholder}
                  className="hero-icon-input"
                  aria-label={txt.passwordLabel}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  className="input-eye-btn"
                  onClick={() => setShowPass(v => !v)}
                  aria-label={showPass ? txt.hidePassword : txt.showPassword}
                >
                  {showPass ? (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M17.94 17.94A10.94 10.94 0 0112 20C6 20 2 12 2 12a18.8 18.8 0 015.06-6.06M9.9 4.24A10.94 10.94 0 0112 4c6 0 10 8 10 8a18.8 18.8 0 01-2.49 3.65M6.53 6.53L17.47 17.47" />
                    </svg>
                  ) : (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M1 12S5 4 12 4s11 8 11 8-4 8-11 8S1 12 1 12z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>

              <button className="hero-get-started-btn hero-signin-btn">
                {txt.signIn} &nbsp;›
              </button>

              <p className="hero-create-link">
                {txt.newHere}{' '}
                <button className="create-account-link" onClick={onCreateAccount}>
                  {txt.createAccount}
                </button>
              </p>
            </section>
          </>
        )}
      </main>
    </div>
  )
}
