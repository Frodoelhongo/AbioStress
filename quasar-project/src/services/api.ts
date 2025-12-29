// src/services/api.ts
import axios from 'axios';

// en desarrollo, FastAPI corre en 127.0.0.1:8000 > abio-stress-twas-backend.biorem.cc
// Detect environment: use localhost backend during local development if applicable
const defaultBase = (typeof window !== 'undefined' && window.location && window.location.hostname && window.location.hostname.includes('localhost'))
  ? 'http://127.0.0.1:8000'
  : (process.env.ABIO_API_URL || 'https://abio-stress-twas-backend.biorem.cc');

export const api = axios.create({
  baseURL: defaultBase,
  timeout: 15000,
});
