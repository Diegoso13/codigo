<template>
  <q-page class="q-pa-lg bg-grey-1">
    <div class="row q-col-gutter-lg">
      <!-- Panel principal -->
      <div class="col-12 col-md-9">
        <q-card class="shadow-3 rounded-borders">
          <q-card-section class="text-white" style="background: #00105b">
            <div class="text-h5 text-weight-bold">Bienvenido a LOLIC</div>

            <div class="text-subtitle1 q-mt-sm">
              Plataforma corporativa para la administración, control y seguimiento de licencias y
              extensiones en EMTELCO.
            </div>
          </q-card-section>

          <q-card-section>
            <div class="text-h6 q-mb-md">Funcionalidades Principales</div>

            <q-list separator>
              <q-item>
                <q-item-section avatar>
                  <q-icon name="verified" color="primary" size="md" />
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-weight-medium"> Gestión de licencias </q-item-label>

                  <q-item-label caption>
                    Registro y seguimiento de licencias corporativas.
                  </q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section avatar>
                  <q-icon name="event_repeat" color="primary" size="md" />
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-weight-medium">
                    Renovaciones y vencimientos
                  </q-item-label>

                  <q-item-label caption> Control de fechas importantes y alertas. </q-item-label>
                </q-item-section>
              </q-item>

              <q-item>
                <q-item-section avatar>
                  <q-icon name="assignment" color="primary" size="md" />
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-weight-medium">
                    Solicitudes y extensiones
                  </q-item-label>

                  <q-item-label caption>
                    Administración centralizada de requerimientos.
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <!-- Agenda -->
      <div class="col-12 col-md-3" v-if="['admin', 'licenciamiento'].includes(rol)">
        <q-card flat class="shadow-3 rounded-borders border-blue">
          <q-card-section
            class="row items-center q-py-sm"
            style="background: #00105b; color: white"
          >
            <q-icon name="event" size="sm" class="q-mr-sm" />

            <div class="text-subtitle1 text-weight-bold">Agenda del Día</div>

            <q-space />

            <q-btn flat round icon="launch" to="/agenda" size="xs" color="white" />
          </q-card-section>

          <q-separator />

          <q-card-section class="q-pa-none" style="max-height: 500px; overflow-y: auto">
            <q-list v-if="actividadesHoy.length > 0" separator>
              <q-item v-for="act in actividadesHoy" :key="act.id">
                <q-item-section avatar>
                  <q-badge rounded :color="act.color === 'Urgente' ? 'red' : 'blue'" />
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-weight-bold text-caption">
                    {{ act.titulo }}
                  </q-item-label>

                  <q-item-label caption>
                    {{ act.descripcion }}
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>

            <div v-else class="column flex-center q-pa-lg text-grey-5">
              <q-icon name="check_circle" size="40px" color="green" />

              <div class="q-mt-sm">Sin actividades pendientes</div>
            </div>
          </q-card-section>

          <q-btn flat full-width label="Ver Calendario Completo" color="primary" to="/agenda" />
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { api } from 'boot/axios'
import { date } from 'quasar'

export default {
  name: 'IndexPage',

  data() {
    return {
      rol: localStorage.getItem('rol'),

      hoy: date.formatDate(Date.now(), 'YYYY-MM-DD'),

      actividadesHoy: [],
    }
  },

  methods: {
    async fetchHoy() {
      if (!['admin', 'licenciamiento'].includes(this.rol)) return

      try {
        const response = await api.get('actividades/')
        this.actividadesHoy = response.data.filter((a) => a.fecha === this.hoy)
      } catch (error) {
        console.error(error)
      }
    },
  },

  mounted() {
    this.fetchHoy()
  },
}
</script>

<style scoped>
.border-blue {
  border: 1px solid #1565c0;
}
</style>
