<template>
  <div class="q-pa-md font-modern">
    <q-layout view="lHh Lpr lff">
      <!-- Toolbar principal con fondo azul oscuro -->
      <q-header elevated class="bg-emtelco-dark text-white">
        <q-toolbar style="height: 55px">
          <q-btn flat round dense icon="menu" @click="drawer = !drawer" />

          <q-space v-if="$q.screen.gt.xs" />

          <q-toolbar-title class="text-center text-weight-bold letter-spacing-2">
            <div class="text-h5 text-weight-bolder letter-spacing-md">LOLIC</div>
          </q-toolbar-title>

          <q-space v-if="$q.screen.gt.xs" />
          <div v-else style="width: 48px"></div>
        </q-toolbar>
      </q-header>

      <!-- Fondo del menú en blanco/claro -->
      <q-drawer
        v-model="drawer"
        show-if-above
        :width="210"
        :breakpoint="400"
        elevated
        class="bg-white"
      >
        <q-scroll-area
          style="
            height: calc(100% - 130px);
            margin-top: 130px;
            border-right: 1px solid rgba(0, 0, 0, 0.05);
          "
        >
          <q-list dense padding class="q-px-sm">
            <!-- Inicio -->
            <q-item clickable v-ripple to="/" class="custom-menu-item q-mb-xs" dense>
              <q-item-section side class="q-pr-xs">
                <q-icon name="dashboard" color="blue-9" size="18px" />
              </q-item-section>
              <q-item-section class="custom-item-text text-dark"> Inicio </q-item-section>
            </q-item>

            <!-- Buscar Licencia-->
            <q-item
              v-if="['licenciamiento', 'admin', 'consulta', 'mesa'].includes(rol)"
              clickable
              v-ripple
              to="/buscar"
              class="custom-menu-item q-mb-xs"
              dense
            >
              <q-item-section side class="q-pr-xs">
                <q-icon name="badge" color="blue-9" size="18px" />
              </q-item-section>
              <q-item-section class="custom-item-text text-dark"> Buscar Licencia</q-item-section>
            </q-item>

            <!-- Buscar Extension-->
            <q-item
              v-if="['licenciamiento', 'admin', 'consulta', 'mesa'].includes(rol)"
              clickable
              v-ripple
              to="/extensiones"
              class="custom-menu-item q-mb-xs"
              dense
            >
              <q-item-section side class="q-pr-xs">
                <q-icon name="find_in_page" color="blue-9" size="18px" />
              </q-item-section>
              <q-item-section class="custom-item-text text-dark"> Buscar Extension</q-item-section>
            </q-item>

            <!-- Desplegable Extensiones -->
            <q-expansion-item
              v-if="['licenciamiento', 'admin'].includes(rol)"
              expand-separator
              dense
              icon="phone_in_talk"
              label="Gestión de Extensiones"
              header-class="custom-expansion-header text-dark"
              class="q-mb-xs custom-expansion text-dark"
            >
              <q-list class="sub-item-list">
                <q-item clickable v-ripple to="/asignarExtension" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="person_add" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Asignar Extensión
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple to="/ReasignarExtension" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="published_with_changes" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Reasignar Extensión
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple to="/TrasladarExtension" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="swap_horizontal_circle" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Intercambiar Extensión
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple to="/LiberarExtension" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="phonelink_erase" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Liberar Extensión
                  </q-item-section>
                </q-item>
              </q-list>
            </q-expansion-item>

            <!-- Desplegable Licencias Office -->
            <q-expansion-item
              v-if="['licenciamiento', 'admin'].includes(rol)"
              expand-separator
              dense
              icon="cloud_queue"
              label="Licencias Office"
              header-class="custom-expansion-header text-dark"
              class="q-mb-xs custom-expansion text-dark"
            >
              <q-list class="sub-item-list">
                <q-item clickable v-ripple to="/Asignar" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="assignment_turned_in" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Asignación de Licencia
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple to="/Traslado" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="move_up" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Traslado de Licencia
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple to="/Recuperacion" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="settings_backup_restore" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Recuperar Licencia
                  </q-item-section>
                </q-item>
              </q-list>
            </q-expansion-item>

            <!-- Desplegable Administrativo -->
            <q-expansion-item
              v-if="['licenciamiento', 'admin'].includes(rol)"
              expand-separator
              dense
              icon="admin_panel_settings"
              label="Administrativo"
              header-class="custom-expansion-header text-dark"
              class="q-mb-xs custom-expansion text-dark"
            >
              <q-list class="sub-item-list">
                <q-item clickable v-ripple to="/Catalogos_licencias" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="auto_stories" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Catalogos Licencias</q-item-section
                  >
                </q-item>

                <q-item
                  clickable
                  v-ripple
                  to="/Catalogos_extensiones"
                  dense
                  class="custom-sub-item"
                >
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="import_contacts" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Catalogos Extensiones</q-item-section
                  >
                </q-item>

                <q-item clickable v-ripple to="/usuarios" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="manage_accounts" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Gestion Usuarios
                  </q-item-section>
                </q-item>

                <q-item clickable v-ripple to="/Gestion" dense class="custom-sub-item">
                  <q-item-section side class="q-pr-xs">
                    <q-icon name="devices" color="blue-9" size="14px" />
                  </q-item-section>
                  <q-item-section class="custom-sub-text text-dark">
                    Gestionar Equipos
                  </q-item-section>
                </q-item>
              </q-list>
            </q-expansion-item>

            <!-- Divider sutil oscuro -->
            <q-separator class="q-my-sm" style="opacity: 0.1" />

            <!-- Agenda de Actividades -->
            <q-item
              v-if="['licenciamiento', 'admin'].includes(rol)"
              clickable
              v-ripple
              to="/agenda"
              class="custom-menu-item q-mb-xs"
              dense
            >
              <q-item-section side class="q-pr-xs">
                <q-icon name="calendar_month" color="blue-9" size="18px" />
              </q-item-section>
              <q-item-section class="custom-item-text text-dark"> Agenda </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>

        <!-- Cabecera de usuario en AZUL OSCURO ORIGINAL con texto blanco -->
        <q-img
          class="absolute-top text-white bg-emtelco-dark"
          style="height: 130px; border-bottom: 1px solid rgba(255, 255, 255, 0.1)"
        >
          <div class="absolute-bottom q-pa-sm bg-transparent flex flex-center column">
            <q-avatar size="38px" class="q-mb-xs shadow-2 bg-white text-blue-9">
              <q-icon name="person" size="22px" />
            </q-avatar>

            <div class="user-text text-white text-center q-mb-xs">
              {{ username }} <span style="opacity: 0.7">({{ rol }})</span>
            </div>

            <q-btn
              outline
              dense
              label="Cerrar sesión"
              color="white"
              class="logout-btn"
              icon="logout"
              size="10px"
              @click="logout"
            />
          </div>
        </q-img>
      </q-drawer>

      <q-page-container>
        <router-view></router-view>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const drawer = ref(false)
    return { drawer }
  },
  data() {
    return {
      rol: localStorage.getItem('rol'),
      username: localStorage.getItem('username'),
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
/* Fuente Base */
.font-modern {
  font-family:
    'Inter',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    sans-serif;
}
.bg-emtelco-dark {
  background-color: #00105b !important;
}

/* Items del Menú */
.custom-menu-item {
  border-radius: 6px;
  min-height: 32px !important;
  transition: background 0.2s ease;
}
.custom-menu-item:hover {
  background: rgba(0, 16, 91, 0.06) !important;
}
.custom-item-text {
  font-size: 12px;
  letter-spacing: 0.2px;
  font-weight: 500;
}

/* Configuración Desplegables e Iconos */
.custom-expansion :deep(.custom-expansion-header) {
  font-size: 12px !important;
  min-height: 32px !important;
  border-radius: 6px;
  padding-left: 8px !important;
}
.custom-expansion :deep(.q-item__section--avatar) {
  min-width: 26px !important;
  padding-right: 0px !important;
  color: #0d47a1 !important; /* Icono principal en azul */
}
.custom-expansion :deep(.q-item__toggle-icon) {
  font-size: 16px !important;
  color: #0d47a1 !important; /* Flecha en azul */
}

/* Sub-ítems Internos */
.sub-item-list {
  margin-left: 16px;
  border-left: 1px solid rgba(0, 0, 0, 0.08);
  padding-left: 4px;
}
.custom-sub-item {
  min-height: 28px !important;
  border-radius: 4px;
  margin-bottom: 2px;
  transition: background 0.2s ease;
}
.custom-sub-item:hover {
  background: rgba(0, 16, 91, 0.04) !important;
}
.custom-sub-text {
  font-size: 11.5px;
}

/* Ajuste de cercanía para todos los iconos side */
:deep(.q-item__section--side) {
  padding-right: 6px !important;
}

/* Sección de Usuario */
.user-text {
  font-size: 11px;
  letter-spacing: 0.3px;
  font-weight: 500;
}
.logout-btn {
  border-radius: 4px;
  text-transform: none;
  width: 85%;
}
.logout-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}
</style>
