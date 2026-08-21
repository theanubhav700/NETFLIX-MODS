import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [backendStatus, setBackendStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Fetch from Node.js backend
    fetch('http://localhost:5000/api/test')
      .then((res) => res.json())
      .then((data) => {
        setBackendStatus(data)
        setLoading(false)
      })
      .catch((err) => {
        setError('❌ Backend se connect nahi ho paya. Ensure backend is running.')
        setLoading(false)
      })
  }, [])

  return (
    <div style={{ textAlign: 'center', marginTop: '80px', fontFamily: 'sans-serif' }}>
      <h1>🚀 Full Stack App</h1>
      <h3>React + Node.js + MongoDB</h3>

      <div style={{
        marginTop: '40px',
        padding: '24px',
        border: '1px solid #ccc',
        borderRadius: '12px',
        display: 'inline-block',
        minWidth: '360px',
        background: '#f9f9f9'
      }}>
        <h4>Backend Connection Status:</h4>

        {loading && <p>⏳ Connecting to backend...</p>}

        {error && (
          <p style={{ color: 'red' }}>{error}</p>
        )}

        {backendStatus && !error && (
          <div>
            <p style={{ color: 'green', fontWeight: 'bold' }}>
              {backendStatus.message}
            </p>
            <p style={{ color: '#555', fontSize: '13px' }}>
              Time: {backendStatus.timestamp}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
