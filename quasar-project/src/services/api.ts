// src/services/api.ts
import axios from 'axios';

// en desarrollo, FastAPI corre en 127.0.0.1:8000 > abio-stress-twas-backend.biorem.cc
export const api = axios.create({
  baseURL: 'https://abio-stress-twas-backend.biorem.cc',
  timeout: 15000,
});
