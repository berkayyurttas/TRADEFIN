// frontend/src/utils/api.ts

import axios from 'axios';

// Flask API'mizin çalıştığı temel URL
const API_BASE_URL = 'http://127.0.0.1:5000/api'; 

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;