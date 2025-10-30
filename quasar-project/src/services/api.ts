// src/services/api.ts
import axios from 'axios';

// en desarrollo, FastAPI corre en 127.0.0.1:8000
export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 15000,
});
