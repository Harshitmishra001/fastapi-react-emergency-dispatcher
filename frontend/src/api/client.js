import axios from 'axios';

// Ponytail: Just point to the local FastAPI server.
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const client = axios.create({
  baseURL: API_URL + '/api/v1',
});

// Intercept requests to add the auth token if available
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
