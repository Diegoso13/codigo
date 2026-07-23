const routes = [
  // Login route
  {
    path: '/login',
    component: () => import('pages/LoginPage.vue'),
  },

  // Main layout with child routes
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue'),
        meta: { roles: ['admin', 'licenciamiento', 'consulta', 'mesa'] },
      },
      {
        path: '/buscar',
        component: () => import('pages/BuscarLicencia.vue'),
        meta: { roles: ['admin', 'licenciamiento', 'consulta', 'mesa'] },
      },

      // LICENCIAS OFFICE
      {
        path: '/Asignar',
        component: () => import('pages/Licenciamiento/AsignarLicencia.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/Traslado',
        component: () => import('pages/Licenciamiento/TrasladoLicencia.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/Recuperacion',
        component: () => import('pages/Licenciamiento/RecuperarLicencia.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },

      // Sección de extensiones
      {
        path: '/extensiones',
        component: () => import('pages/Extensiones/extensionesListPage.vue'),
      },
      {
        path: '/asignarExtension',
        component: () => import('pages/Extensiones/AsignarExtension.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/ReasignarExtension',
        component: () => import('pages/Extensiones/ReasignarExtension.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/TrasladarExtension',
        component: () => import('pages/Extensiones/TrasladarExtension.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/LiberarExtension',
        component: () => import('pages/Extensiones/LiberarExtension.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/movimientos_extensiones',
        component: () => import('pages/Extensiones/lmovimientoslistPage.vue'),
      },

      // ADMINSTRATIVO
      {
        path: '/catalogos_licencias',
        component: () => import('pages/Administrativo/CatalogosPage.vue'),
        meta: { roles: ['admin'] },
      },
      {
        path: '/catalogos_extensiones',
        component: () => import('pages/Administrativo/catalogsListPage.vue'),
      },
      {
        path: '/usuarios',
        component: () => import('pages/Administrativo/listUsuarioPage.vue'),
        meta: { roles: ['admin'] },
      },
      {
        path: '/Gestion',
        component: () => import('pages/Administrativo/GestionEquipos.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
      {
        path: '/agenda',
        component: () => import('pages/AgendaPage.vue'),
        meta: { roles: ['admin', 'licenciamiento'] },
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
]

export default routes
