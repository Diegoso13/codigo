import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  // UNIFICACIÓN DE TODA LA LÓGICA DE SEGURIDAD
  Router.beforeEach((to) => {
    const token = localStorage.getItem('token')
    const rol = localStorage.getItem('rol')
    const ahora = Date.now()
    const ultimoAcceso = localStorage.getItem('ultimoAcceso')
    const TIEMPO_LIMITE = 15 * 60 * 1000 // 15 minutos

    // --- 1. CONTROL DE INACTIVIDAD (Solo si ya está logueado) ---
    if (token && ultimoAcceso) {
      if (ahora - ultimoAcceso > TIEMPO_LIMITE) {
        localStorage.removeItem('token')
        localStorage.removeItem('rol')
        localStorage.removeItem('ultimoAcceso')
        return '/login'
      }
    }

    // --- 2. ACCESO AL LOGIN ---
    if (to.path === '/login') {
      if (token) return '/' // Si ya tiene token, lo mandamos al inicio
      return true // Si no tiene token, lo dejamos entrar al login
    }

    // --- 3. PROTECCIÓN DE RUTAS (Requieren Token) ---
    if (!token) {
      return '/login' // Si no hay token y no es login, para afuera
    }

    // --- 4. PROTECCIÓN POR ROLES ---
    if (to.meta.roles) {
      const tienePermiso = to.meta.roles.includes(rol)
      if (!tienePermiso) {
        // Si no tiene permiso, intentamos mandarlo al Home, si ya está ahí, al Login
        return to.path === '/' ? '/login' : '/'
      }
    }

    // --- 5. ACTUALIZACIÓN DE ACTIVIDAD Y ÉXITO ---
    // Si llegó hasta aquí, la navegación es válida
    if (token) {
      localStorage.setItem('ultimoAcceso', ahora)
    }

    return true
  })

  return Router
})
