import axios, { type AxiosError } from 'axios'
import toast from 'react-hot-toast'
import { useAuthStore } from '@/store/authStore'
import { ROUTES } from '@/constants/routes'

/** In development, use the Vite /api proxy. Production can override VITE_API_BASE_URL. */
const envBaseURL = (import.meta.env.VITE_API_BASE_URL ?? '').trim().replace(/\/$/, '')
const baseURL =
  envBaseURL ||
  '/api/v1/web_api'

export const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
})

function redirectAfterAuthFailure() {
  const path = window.location.pathname
  if (path.startsWith(ROUTES.dashboard)) {
    window.location.assign(ROUTES.error401)
    return
  }
  if (!path.startsWith(ROUTES.login)) {
    window.location.assign(ROUTES.login)
  }
}

axiosInstance.interceptors.request.use((config) => {
  const { accessToken: token, tokenType } = useAuthStore.getState()
  if (token) {
    const type = tokenType ?? 'Bearer'
    config.headers.Authorization = `${type} ${token}`
  }
  return config
})

axiosInstance.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const status = error.response?.status

    if (status && status >= 500) {
      toast.error('Server error. Please try again.')
    }

    // The researcher API uses a normal expiring bearer token and has no
    // separate refresh endpoint. A 401 therefore ends the local session.
    if (status === 401) {
      const url = error.config?.url ?? ''
      if (!url.includes('/auth/login') && !url.includes('/auth/register')) {
        useAuthStore.getState().logout()
        redirectAfterAuthFailure()
      }
    }

    return Promise.reject(error)
  }
)
