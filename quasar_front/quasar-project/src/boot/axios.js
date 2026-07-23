import { boot } from 'quasar/wrappers'
import axios from 'axios'
import { Notify } from 'quasar'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/',
})

export default boot(({ app }) => {
  app.config.globalProperties.$api = api
})

// --- INTERCEPTOR DE PETICIÓN ---
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')

    // Si es login (ajustado a tu nueva ruta 'auth/login'), no tocamos nada
    if (config.url.includes('auth/login')) return config

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// --- INTERCEPTOR DE RESPUESTA ---
let isExpiring = false

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 1. Detectar si el error viene de un intento de LOGIN
    // Usamos el include para capturar 'auth/login'
    const isLoginAction = error.config?.url?.includes('auth/login')

    // 2. Si el error es 401 o 403
    if (error.response && [401, 403].includes(error.response.status)) {
      // SI ES LOGIN: No mostrar "Sesión expirada", simplemente rechazar
      // para que el componente muestre "Usuario o clave incorrecta"
      if (isLoginAction) {
        return Promise.reject(error)
      }

      // SI NO ES LOGIN (Cualquier otro módulo): Aplicar lógica de expulsión
      if (isExpiring) return Promise.reject(error)

      isExpiring = true

      localStorage.removeItem('token')
      localStorage.removeItem('rol')
      localStorage.removeItem('username')
      localStorage.removeItem('ultimoAcceso')

      Notify.create({
        type: 'warning',
        message: 'Su sesión ha expirado, inicie sesión nuevamente.',
        position: 'top',
        timeout: 4000,
      })

      setTimeout(() => {
        window.location.href = '/#/login'
        isExpiring = false
      }, 1000)
    }

    return Promise.reject(error)
  },
)

export { api }
