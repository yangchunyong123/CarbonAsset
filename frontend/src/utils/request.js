import axios from "axios";
import { useAuthStore } from "../stores/auth";

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  timeout: 15000,
});

/**
 * Attach JWT token to every outbound request when available.
 */
request.interceptors.request.use((config) => {
  const store = useAuthStore();
  if (store.accessToken) {
    config.headers.Authorization = `Bearer ${store.accessToken}`;
  }
  return config;
});

/**
 * Normalize API response and handle token expiration centrally.
 */
request.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const store = useAuthStore();
    if (error?.response?.status === 401) {
      store.logout();
      location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default request;
