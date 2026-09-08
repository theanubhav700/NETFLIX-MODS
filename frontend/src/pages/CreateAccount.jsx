import { useState } from 'react'
import './CreateAccount.css'

const EyeOpen = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
    strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12S5 4 12 4s11 8 11 8-4 8-11 8S1 12 1 12z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
)

const EyeOff = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
    strokeLinecap="round" strokeLinejoin="round">
    <path d="M17.94 17.94A10.94 10.94 0 0112 20C6 20 2 12 2 12a18.8 18.8 0 015.06-6.06M9.9 4.24A10.94 10.94 0 0112 4c6 0 10 8 10 8a18.8 18.8 0 01-2.49 3.65M6.53 6.53L17.47 17.47" />
  </svg>
)

const FEATURES = [
  { icon: '🎬', text: 'Stream thousands of exclusive movies & shows' },
  { icon: '📱', text: 'Watch on any device — TV, phone, laptop, tablet' },
  { icon: '⚡', text: 'HD & 4K quality with zero ads' },
  { icon: '🔒', text: 'Secure account with parental controls' },
]

export default function CreateAccount({ onBack }) {
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '' })
  const [showPass, setShowPass]       = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [errors, setErrors]           = useState({})
  const [submitted, setSubmitted]     = useState(false)

  const update = (field) => (e) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }))

  const validate = () => {
    const e = {}
    if (!form.name.trim())               e.name     = 'Full name is required'
    if (!form.email.includes('@'))       e.email    = 'Enter a valid email address'
    if (form.password.length < 6)        e.password = 'Minimum 6 characters'
    if (form.password !== form.confirm)  e.confirm  = 'Passwords do not match'
    return e
  }

  const handleSubmit = (ev) => {
    ev.preventDefault()
    const e = validate()
    if (Object.keys(e).length) { setErrors(e); return }
    setErrors({})
    setSubmitted(true)
  }

  /* ── Success screen ── */
  if (submitted) {
    return (
      <div className="ca-root">
        <div className="ca-success-full">
          <div className="ca-success-glow" />
          <div className="ca-success-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2"
              strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <path d="M7 12.5l3.5 3.5 6.5-7" />
            </svg>
          </div>
          <h2 className="ca-success-title">Account Created!</h2>
          <p className="ca-success-sub">
            Welcome to <span className="ca-red">Netflix Mods</span>,{' '}
            <strong>{form.name}</strong>. You're all set to start watching.
          </p>
          <button className="ca-btn-primary" onClick={onBack}>Go to Sign In →</button>
        </div>
      </div>
    )
  }

  /* ── Main layout ── */
  return (
    <div className="ca-root">
      {/* ── LEFT PANEL ── */}
      <div className="ca-left">
        {/* blobs */}
        <div className="ca-blob ca-blob-1" />
        <div className="ca-blob ca-blob-2" />
        <div className="ca-blob ca-blob-3" />

        <div className="ca-left-inner">
          <div className="ca-brand">NETFLIX MODS</div>

          <h1 className="ca-hero-title">
            Your world<br />
            of <span className="ca-red">entertainment</span><br />
            starts here.
          </h1>
          <p className="ca-hero-sub">
            Create a free account and unlock unlimited streaming, exclusive content,
            and personalised recommendations — all in one place.
          </p>

          <ul className="ca-features">
            {FEATURES.map((f, i) => (
              <li key={i} className="ca-feature-item">
                <span className="ca-feat-icon">{f.icon}</span>
                <span>{f.text}</span>
              </li>
            ))}
          </ul>

          <div className="ca-stats">
            <div className="ca-stat">
              <span className="ca-stat-num">200M+</span>
              <span className="ca-stat-label">Members</span>
            </div>
            <div className="ca-stat-divider" />
            <div className="ca-stat">
              <span className="ca-stat-num">190+</span>
              <span className="ca-stat-label">Countries</span>
            </div>
            <div className="ca-stat-divider" />
            <div className="ca-stat">
              <span className="ca-stat-num">15K+</span>
              <span className="ca-stat-label">Titles</span>
            </div>
          </div>
        </div>
      </div>

      {/* ── RIGHT PANEL ── */}
      <div className="ca-right">
        <div className="ca-form-panel">
          {/* back button */}
          <button className="ca-back-btn" onClick={onBack} aria-label="Go back">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
              strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 12H5M12 5l-7 7 7 7" />
            </svg>
            Back
          </button>

          <div className="ca-form-header">
            <h2 className="ca-form-title">Create Account</h2>
            <p className="ca-form-sub">Join millions watching today.</p>
          </div>

          <form className="ca-form" onSubmit={handleSubmit} noValidate>

            {/* Full Name */}
            <div className={`ca-field ${errors.name ? 'ca-field--error' : ''}`}>
              <label className="ca-label" htmlFor="ca-name">Full Name</label>
              <div className="ca-input-wrap">
                <span className="ca-input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                    strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="8" r="4" />
                    <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
                  </svg>
                </span>
                <input
                  id="ca-name" type="text" className="ca-input"
                  placeholder="John Doe" value={form.name}
                  onChange={update('name')} autoComplete="name"
                />
              </div>
              {errors.name && <span className="ca-error">{errors.name}</span>}
            </div>

            {/* Email */}
            <div className={`ca-field ${errors.email ? 'ca-field--error' : ''}`}>
              <label className="ca-label" htmlFor="ca-email">Email Address</label>
              <div className="ca-input-wrap">
                <span className="ca-input-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                    strokeLinecap="round" strokeLinejoin="round">
                    <rect x="2" y="4" width="20" height="16" rx="2" />
                    <path d="M2 7l10 7 10-7" />
                  </svg>
                </span>
                <input
                  id="ca-email" type="email" className="ca-input"
                  placeholder="you@example.com" value={form.email}
                  onChange={update('email')} autoComplete="email"
                />
              </div>
              {errors.email && <span className="ca-error">{errors.email}</span>}
            </div>

            {/* Password + Confirm side by side */}
            <div className="ca-row-two">
              {/* Password */}
              <div className={`ca-field ${errors.password ? 'ca-field--error' : ''}`}>
                <label className="ca-label" htmlFor="ca-pass">Password</label>
                <div className="ca-input-wrap">
                  <span className="ca-input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                      strokeLinecap="round" strokeLinejoin="round">
                      <rect x="5" y="11" width="14" height="10" rx="2" />
                      <path d="M8 11V7a4 4 0 018 0v4" />
                      <circle cx="12" cy="16" r="1.2" fill="currentColor" stroke="none" />
                    </svg>
                  </span>
                  <input
                    id="ca-pass" type={showPass ? 'text' : 'password'} className="ca-input"
                    placeholder="Min. 6 chars" value={form.password}
                    onChange={update('password')} autoComplete="new-password"
                  />
                  <button type="button" className="ca-eye-btn"
                    onClick={() => setShowPass(v => !v)}
                    aria-label={showPass ? 'Hide' : 'Show'}>
                    {showPass ? <EyeOff /> : <EyeOpen />}
                  </button>
                </div>
                {errors.password && <span className="ca-error">{errors.password}</span>}
              </div>

              {/* Confirm */}
              <div className={`ca-field ${errors.confirm ? 'ca-field--error' : ''}`}>
                <label className="ca-label" htmlFor="ca-confirm">Confirm Password</label>
                <div className="ca-input-wrap">
                  <span className="ca-input-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
                      strokeLinecap="round" strokeLinejoin="round">
                      <rect x="5" y="11" width="14" height="10" rx="2" />
                      <path d="M8 11V7a4 4 0 018 0v4" />
                      <path d="M9.5 16l2 2 3-3" />
                    </svg>
                  </span>
                  <input
                    id="ca-confirm" type={showConfirm ? 'text' : 'password'} className="ca-input"
                    placeholder="Repeat password" value={form.confirm}
                    onChange={update('confirm')} autoComplete="new-password"
                  />
                  <button type="button" className="ca-eye-btn"
                    onClick={() => setShowConfirm(v => !v)}
                    aria-label={showConfirm ? 'Hide' : 'Show'}>
                    {showConfirm ? <EyeOff /> : <EyeOpen />}
                  </button>
                </div>
                {errors.confirm && <span className="ca-error">{errors.confirm}</span>}
              </div>
            </div>

            {/* Terms */}
            <p className="ca-terms">
              By creating an account you agree to our{' '}
              <span className="ca-link">Terms of Service</span> and{' '}
              <span className="ca-link">Privacy Policy</span>.
            </p>

            <button type="submit" className="ca-btn-primary ca-btn-full">
              Create Account
            </button>
          </form>

          <p className="ca-signin-row">
            Already have an account?{' '}
            <button className="ca-signin-link" onClick={onBack}>Sign In</button>
          </p>
        </div>
      </div>
    </div>
  )
}
