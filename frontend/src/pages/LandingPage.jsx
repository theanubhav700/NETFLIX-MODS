import { useState, useEffect } from 'react'
import './LandingPage.css'

// Detect karo ki app mein hai ya website pe
const isNativeApp = () => {
  try {
    return window.Capacitor && window.Capacitor.isNativePlatform()
  } catch {
    return false
  }
}

const T = {
  English: {
    brand:          'NETMUSIC',
    accountRequest: 'GET PREMIUM',
    heroTitle:      <>Unlimited music,<br />podcasts, and more</>,
    heroSub:        'Listen anywhere, anytime.',
    heroCta:        'Ready to listen? Sign in or create a free account.',
    emailPlaceholder:    'Email address',
    emailLabel:          'Email address',
    passwordPlaceholder: 'Password',
    passwordLabel:       'Password',
    signIn:         'Sign In',
    newHere:        'New here?',
    createAccount:  'Create a free account',
    showPassword:   'Show password',
    hidePassword:   'Hide password',
  },
}

const REASONS = [
  {
    title: 'Ad-Free Music',
    desc:  'Enjoy unlimited songs without a single interruption. Pure music, zero ads.',
    icon:  '🎵',
  },
  {
    title: 'Listen Offline',
    desc:  'Download your favourite tracks and playlists. Play without internet.',
    icon:  '📥',
  },
  {
    title: 'Hi-Fi Audio Quality',
    desc:  'Experience studio-grade sound with lossless & high-bitrate streaming.',
    icon:  '🎧',
  },
  {
    title: 'Cross-Device Sync',
    desc:  'Seamlessly switch between phone, tablet, laptop and smart speakers.',
    icon:  '📱',
  },
]

const TRENDING = [
  { rank: '01', label: 'Blinding Lights',  color: '#1a0a2e' },
  { rank: '02', label: 'Levitating',       color: '#0a1a2e' },
  { rank: '03', label: 'Stay',             color: '#1a1a0a' },
  { rank: '04', label: 'Heat Waves',       color: '#0a1a1a' },
  { rank: '05', label: 'As It Was',        color: '#1a0a0a' },
  { rank: '06', label: 'Flowers',          color: '#0a0a1a' },
  { rank: '07', label: 'Cruel Summer',     color: '#1a150a' },
  { rank: '08', label: 'Anti-Hero',        color: '#150a1a' },
]

export default function LandingPage({ onCreateAccount, onSignIn }) {
  const [loading, setLoading]     = useState(true)
  const [email, setEmail]         = useState('')
  const [password, setPassword]   = useState('')
  const [showPass, setShowPass]   = useState(false)
  const [signInError, setSignInError] = useState('')

  // drag-scroll state
  const [isDragging, setIsDragging] = useState(false)
  const [startX, setStartX]         = useState(0)
  const [scrollLeft, setScrollLeft] = useState(0)

  const txt = T.English

  // ── Sign In handler ──
  const handleSignIn = () => {
    setSignInError('')
    if (!email.trim()) { setSignInError('Please enter your email.'); return }
    if (!password)     { setSignInError('Please enter your password.'); return }

    const accounts = JSON.parse(localStorage.getItem('nm_accounts') || '[]')
    const match = accounts.find(
      a => a.email.toLowerCase() === email.trim().toLowerCase() && a.password === password
    )
    if (!match) {
      setSignInError('Incorrect email or password. Please try again.')
      return
    }
    // save current user and proceed to greeting
    localStorage.setItem('nm_current_user', JSON.stringify({ name: match.name, email: match.email }))
    onSignIn(match.name)
  }

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 2500)
    return () => clearTimeout(timer)
  }, [])

  const onMouseDown = (e) => {
    setIsDragging(true)
    setStartX(e.pageX - e.currentTarget.offsetLeft)
    setScrollLeft(e.currentTarget.scrollLeft)
  }
  const onMouseMove = (e) => {
    if (!isDragging) return
    e.preventDefault()
    const x    = e.pageX - e.currentTarget.offsetLeft
    const walk = (x - startX) * 1.4
    e.currentTarget.scrollLeft = scrollLeft - walk
  }
  const stopDrag = () => setIsDragging(false)

  return (
    <div className="landing-root">
      {/* ── Navbar ── */}
      <nav className="landing-nav">
        <div className="landing-logo">
          <span className="brand-logo">{txt.brand}</span>
        </div>
        <div className="landing-nav-right">
          {!isNativeApp() && (
            <a
              href="/NETMUSIC.apk"
              download="NETMUSIC.apk"
              className="download-apk-btn"
              aria-label="Download Android App"
            >
              ⬇ DOWNLOAD APP
            </a>
          )}
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
            {/* ── Hero ── */}
            <section className="hero-content">
              <h1 className="hero-title">{txt.heroTitle}</h1>
              <p className="hero-sub">{txt.heroSub}</p>
              <p className="hero-cta-text">{txt.heroCta}</p>

              {/* Email input */}
              <div className="hero-input-group">
                <span className="input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                    strokeLinecap="round" strokeLinejoin="round">
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
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                    strokeLinecap="round" strokeLinejoin="round">
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
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                      strokeLinecap="round" strokeLinejoin="round">
                      <path d="M17.94 17.94A10.94 10.94 0 0112 20C6 20 2 12 2 12a18.8 18.8 0 015.06-6.06M9.9 4.24A10.94 10.94 0 0112 4c6 0 10 8 10 8a18.8 18.8 0 01-2.49 3.65M6.53 6.53L17.47 17.47" />
                    </svg>
                  ) : (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                      strokeLinecap="round" strokeLinejoin="round">
                      <path d="M1 12S5 4 12 4s11 8 11 8-4 8-11 8S1 12 1 12z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>

              <button className="hero-get-started-btn hero-signin-btn" onClick={handleSignIn}>
                {txt.signIn} &nbsp;›
              </button>

              {signInError && (
                <p className="signin-error">{signInError}</p>
              )}

              <p className="hero-create-link">
                {txt.newHere}{' '}
                <button className="create-account-link" onClick={onCreateAccount}>
                  {txt.createAccount}
                </button>
              </p>
            </section>

            {/* ── Reasons section ── */}
            <section className="reasons-section" aria-label="Why NETMUSIC">
              <h2 className="section-heading">More reasons to join</h2>
              <div className="reasons-grid">
                {REASONS.map((r, i) => (
                  <div className="reason-card" key={i}>
                    <div className="reason-card-top">
                      <p className="reason-title">{r.title}</p>
                      <p className="reason-desc">{r.desc}</p>
                    </div>
                    <div className="reason-icon-wrap">
                      <span className="feat-icon" aria-hidden="true"
                        style={{ fontSize: 42, lineHeight: 1 }}>
                        {r.icon}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* ── Trending Now ── */}
            <section className="trending-section" aria-label="Trending Now">
              <h2 className="section-heading">🔥 Trending Now</h2>
              <div
                className={`trending-track ${isDragging ? 'dragging' : ''}`}
                onMouseDown={onMouseDown}
                onMouseMove={onMouseMove}
                onMouseUp={stopDrag}
                onMouseLeave={stopDrag}
              >
                {TRENDING.map((t, i) => (
                  <div
                    className="trending-card"
                    key={i}
                    style={{ '--card-bg': t.color }}
                    aria-label={t.label}
                  >
                    <span className="trending-rank">{t.rank}</span>
                    <span className="trending-label">{t.label}</span>
                    <span className="trending-play" aria-hidden="true">
                      <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    </span>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  )
}
