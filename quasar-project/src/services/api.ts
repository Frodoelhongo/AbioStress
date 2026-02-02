// src/services/api.ts
import axios from 'axios';

// En desarrollo, FastAPI corre en el mismo host pero puerto 8000.
// En producción, usar el backend público.
const windowAvailable = typeof window !== 'undefined' && !!window.location;
const hostname = windowAvailable ? window.location.hostname : '';

const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '0.0.0.0' || hostname === '::1';
const isProdHost = hostname === 'abio-stress-twas.biorem.cc';

const envBase = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_ABIO_API_URL)
  ? import.meta.env.VITE_ABIO_API_URL
  : (typeof process !== 'undefined' && process.env && process.env.ABIO_API_URL)
    ? process.env.ABIO_API_URL
    : '';

const defaultBase = envBase
  ? envBase
  : windowAvailable
    ? (isProdHost
      ? 'https://abio-stress-twas-backend.biorem.cc'
      : (isLocalhost ? 'http://127.0.0.1:8000' : `http://${hostname}:8000`))
    : 'https://abio-stress-twas-backend.biorem.cc';

export const api = axios.create({
  baseURL: defaultBase,
  timeout: 15000,
});
