import axios from 'axios';

const host = import.meta.env.VITE_APP_HOST

const api = axios.create({
  baseURL: 'host',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

export default api;
