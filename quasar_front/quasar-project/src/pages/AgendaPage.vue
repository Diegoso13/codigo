<template>
  <q-page class="q-pa-lg bg-grey-1">
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-md-4">
        <q-card flat class="rounded-borders shadow-2 full-height">
          <q-card-section class="bg-blue-9 text-white">
            <div class="text-h6 text-center">Calendario de Actividades</div>
          </q-card-section>

          <q-date
            v-model="selectedDate"
            :events="eventDates"
            event-color="orange"
            flat
            full-width
            class="no-shadow calendario-gigante"
            @update:model-value="filterActivities"
          />
        </q-card>
      </div>

      <div class="col-12 col-md-8">
        <q-card flat class="rounded-borders shadow-2" style="min-height: 500px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h5 text-weight-bold">Actividades del {{ selectedDate || '...' }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nueva Actividad"
              @click="showDialog = true"
              unelevated
            />
          </q-card-section>

          <q-separator q-mt-md />

          <q-card-section>
            <q-list v-if="filteredActivities.length > 0" separator>
              <q-item v-for="act in filteredActivities" :key="act.id" class="q-py-md">
                <q-item-section avatar>
                  <q-icon
                    :name="act.color === 'Realizado' ? 'check_circle' : 'event_available'"
                    :color="act.color === 'Realizado' ? 'positive' : 'blue-9'"
                    size="md"
                  />
                </q-item-section>

                <q-item-section>
                  <q-item-label
                    class="text-weight-bold text-subtitle1"
                    :class="{ 'text-strike text-grey-6': act.color === 'Realizado' }"
                  >
                    {{ act.titulo }}
                  </q-item-label>
                  <q-item-label caption class="text-grey-8">{{ act.descripcion }}</q-item-label>
                </q-item-section>

                <q-item-section side>
                  <div class="row q-gutter-xs no-wrap">
                    <q-btn
                      flat
                      round
                      dense
                      :icon="act.color === 'Realizado' ? 'task_alt' : 'radio_button_unchecked'"
                      :color="act.color === 'Realizado' ? 'positive' : 'grey-7'"
                      @click="toggleDone(act)"
                    />
                    <q-btn flat round dense icon="edit" color="blue-9" @click="editActivity(act)" />
                    <q-btn
                      flat
                      round
                      dense
                      icon="delete"
                      color="negative"
                      @click="confirmDelete(act)"
                    />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>

            <div v-else class="column flex-center q-pa-xl text-grey-6">
              <q-icon name="event_busy" size="80px" />
              <div class="text-h6 q-mt-md">No hay actividades para esta fecha</div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <q-dialog v-model="showDialog">
      <q-card style="width: 400px">
        <q-card-section class="bg-blue-9 text-white">
          <div class="text-h6">Registrar Actividad</div>
        </q-card-section>

        <q-card-section class="q-gutter-md">
          <q-input filled v-model="newActivity.titulo" label="Título" />
          <q-input filled v-model="newActivity.descripcion" label="Descripción" type="textarea" />
          <q-input filled v-model="newActivity.fecha" label="Fecha" mask="date">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                  <q-date v-model="newActivity.fecha">
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Cerrar" color="primary" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="grey" v-close-popup />
          <q-btn unelevated label="Guardar" color="primary" @click="saveActivity" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { api } from 'boot/axios'
import { date } from 'quasar'

export default {
  data() {
    return {
      selectedDate: date.formatDate(Date.now(), 'YYYY/MM/DD'),
      showDialog: false,
      allActivities: [],
      filteredActivities: [],
      eventDates: [],
      // Estas dos deben ir afuera para que this.isEditing funcione
      isEditing: false,
      currentId: null,
      newActivity: {
        titulo: '',
        descripcion: '',
        fecha: date.formatDate(Date.now(), 'YYYY/MM/DD'),
        color: 'Normal',
      },
    }
  },

  methods: {
    filterActivities() {
      // <--- Revisa que no falte la 's' o tenga errores de dedo
      const selected = this.selectedDate.replace(/\//g, '-')
      this.filteredActivities = this.allActivities.filter((a) => a.fecha === selected)
    },
    async fetchActivities() {
      try {
        // Usamos la ruta relativa al baseURL definido en axios.js
        // Si tu baseURL ya tiene 'api/', aquí solo va 'actividades/'
        const response = await api.get('actividades/')
        this.allActivities = response.data
        this.eventDates = this.allActivities.map((a) => a.fecha.replace(/-/g, '/'))
        this.filterActivities()
      } catch (err) {
        console.error('Error al cargar:', err) // <--- Aquí ya la estás usando
        this.$q.notify({ type: 'negative', message: 'Error al cargar agenda' })
      }
    },

    // 1. Preparar el diálogo para editar
    editActivity(act) {
      this.isEditing = true // Ahora sí existe en 'this'
      this.currentId = act.id
      this.newActivity = {
        titulo: act.titulo,
        descripcion: act.descripcion,
        fecha: act.fecha.replace(/-/g, '/'),
        color: act.color,
      }
      this.showDialog = true
    },

    // 2. Método para marcar como realizado rápidamente
    async toggleDone(act) {
      try {
        const nuevoEstado = act.color === 'Realizado' ? 'Normal' : 'Realizado'

        // 1. Mandamos el cambio al servidor
        await api.patch(`actividades/${act.id}/`, { color: nuevoEstado })

        // 2. CAMBIO CLAVE: Buscamos el ítem exacto en nuestra lista local y lo actualizamos
        // Esto evita que Vue tenga que redibujar toda la lista y previene duplicados visuales
        const index = this.allActivities.findIndex((item) => item.id === act.id)
        if (index !== -1) {
          this.allActivities[index].color = nuevoEstado
        }

        // 3. Refrescar el filtro para que se vea el cambio en pantalla
        this.filterActivities()

        this.$q.notify({
          type: 'positive',
          message: 'Estado actualizado',
          timeout: 800,
        })
      } catch (err) {
        console.error('Error al actualizar:', err)
        this.$q.notify({ type: 'negative', message: 'No se pudo actualizar el estado' })
      }
    },

    // 3. Modificar el saveActivity para que decida si crear o actualizar
    async saveActivity() {
      try {
        const dataToSend = {
          titulo: this.newActivity.titulo,
          descripcion: this.newActivity.descripcion,
          fecha: this.newActivity.fecha.replace(/\//g, '-'),
          color: this.newActivity.color,
        }

        if (this.isEditing) {
          // Petición PUT para actualizar
          await api.put(`actividades/${this.currentId}/`, dataToSend)
          this.$q.notify({ type: 'positive', message: 'Actividad actualizada' })
        } else {
          // Petición POST para crear
          await api.post('actividades/', dataToSend)
          this.$q.notify({ type: 'positive', message: 'Actividad registrada' })
        }

        this.resetForm()
        this.fetchActivities()
      } catch (err) {
        console.error('Error al guardar:', err) // <--- Uso de la variable
        this.$q.notify({ type: 'negative', message: 'No se pudo guardar la actividad' })
      }
    },

    // 4. Confirmar y eliminar
    confirmDelete(act) {
      this.$q
        .dialog({
          title: 'Confirmar eliminación',
          message: `¿Estás seguro de eliminar "${act.titulo}"?`,
          cancel: true,
          persistent: true,
        })
        .onOk(async () => {
          try {
            await api.delete(`actividades/${act.id}/`)
            this.$q.notify({ type: 'positive', message: 'Actividad eliminada' })
            this.fetchActivities()
          } catch (err) {
            console.error('Error en la operación:', err) // <--- Uso de la variable
            this.$q.notify({ type: 'negative', message: 'Error en el servidor' })
          }
        })
    },

    // Limpiar el formulario
    resetForm() {
      this.showDialog = false
      this.isEditing = false
      this.currentId = null
      this.newActivity = {
        titulo: '',
        descripcion: '',
        fecha: date.formatDate(Date.now(), 'YYYY/MM/DD'),
        color: 'Normal',
      }
    },
  },

  mounted() {
    this.fetchActivities()
  },
}
</script>

<style scoped>
.border-blue {
  border: 1px solid #1565c0;
}

/* Forzamos al calendario a ocupar todo el ancho disponible */
.calendario-gigante {
  width: 100% !important;
  max-width: none !important; /* Quita el límite de Quasar */
  min-height: 450px; /* Ajusta este valor según qué tan alto lo quieras */
}

/* Opcional: Agrandar un poco más los números y el texto del calendario */
:deep(.q-date__calendar-item) {
  padding: 4px; /* Espaciado entre días */
}

:deep(.q-date__calendar-days-container) {
  min-height: 300px; /* Hace que el cuerpo del calendario sea más alto */
}
</style>
