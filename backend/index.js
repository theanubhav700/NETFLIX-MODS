const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const connectDB = require('./config/db');

// Load environment variables
dotenv.config();

// Connect to MongoDB
connectDB();

const app = express();

// ─── Middleware ───────────────────────────────────────────────
// CORS: Allow React frontend (port 5173) to communicate with backend
app.use(cors({
  origin: 'http://localhost:5173',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true,
}));

// Parse incoming JSON requests
app.use(express.json());

// ─── Routes ──────────────────────────────────────────────────
// Health check route — verify backend is running
app.get('/', (req, res) => {
  res.json({ message: '🚀 Backend is running!', status: 'OK' });
});

// API test route — verify frontend-backend connection
app.get('/api/test', (req, res) => {
  res.json({
    message: '✅ React → Node.js → MongoDB connection successful!',
    timestamp: new Date().toISOString(),
  });
});

// ─── Start Server ─────────────────────────────────────────────
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
