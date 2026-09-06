import { useState } from 'react'
import './TermsPage.css'

export default function TermsPage({ onAccept }) {
  const [agreed, setAgreed] = useState(false)

  return (
    <div className="terms-root">
      {/* Centered glass card */}
      <div className="terms-card">
        {/* Title */}
        <h1 className="terms-title">
          NETFLIX MODS<br />Terms &amp; Conditions
        </h1>

        {/* Divider */}
        <div className="terms-divider" />

        {/* Intro */}
        <p className="terms-intro">
          By accessing or using the NETFLIX MODS platform, its content,
          brand assets, logos, or any associated materials ("Platform Assets"),
          you ("You" or "User") agree to be bound by the following Terms &amp;
          Conditions ("Terms"). In the event of any conflict between these Terms
          and any other written agreement between You and NETFLIX MODS,
          the written agreement shall prevail.
        </p>

        {/* Divider */}
        <div className="terms-divider" />

        {/* Checkbox */}
        <label className="terms-checkbox-label">
          <input
            type="checkbox"
            className="terms-checkbox"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            aria-label="I agree to the Terms and Conditions"
          />
          <span>
            I have read and agree to the{' '}
            <strong>Terms &amp; Conditions</strong> of NETFLIX MODS.
          </span>
        </label>

        {/* Button */}
        <button
          className={`terms-continue-btn ${agreed ? 'active' : ''}`}
          disabled={!agreed}
          onClick={onAccept}
        >
          Continue to Platform &nbsp;›
        </button>
      </div>
    </div>
  )
}
