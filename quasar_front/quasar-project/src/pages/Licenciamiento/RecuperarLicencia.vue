<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Recuperar licencia</div>

        <div class="asig-header__sub">Seleccione un equipo para recuperar su licencia</div>
      </div>
    </div>

    <!-- FORM -->
    <q-card class="shadow-card rounded-card">
      <q-card-section>
        <div class="text-subtitle1 text-weight-bold q-mb-md">Datos de recuperación</div>

        <div class="row q-col-gutter-md">
          <!-- EQUIPO -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="equipoSeleccionado"
              use-input
              input-debounce="300"
              label="Seleccionar equipo para recuperar"
              :options="equipos"
              option-label="nombre_equipo"
              @filter="buscarEquipos"
              @update:model-value="cargarLicencia"
              clearable
              @clear="software = ''"
              @keydown="bloquearEscritura"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="computer" />
              </template>
            </q-select>
          </div>

          <!-- LICENCIA -->
          <div class="col-12 col-md-6">
            <q-input v-model="software" label="Licencia a recuperar" readonly outlined dense>
              <template #prepend>
                <q-icon name="vpn_key" />
              </template>
            </q-input>
          </div>

          <!-- TICKET -->
          <div class="col-12 col-md-6">
            <q-input
              v-model="ticket"
              label="Ticket de retiro/recuperación"
              type="number"
              class="no-spinner"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="confirmation_number" />
              </template>
            </q-input>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- ACTIONS -->
      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          label="Recuperar licencia"
          color="primary"
          unelevated
          class="btn-action"
          :disable="!equipoSeleccionado || !software || !ticket"
          @click="recuperar"
        />
      </q-card-actions>
    </q-card>

    <!-- RESULTADO -->
    <q-card v-if="registroGenerado" class="shadow-card rounded-card q-mt-md">
      <q-card-section>
        <div class="text-weight-bold q-mb-sm">Registro de recuperación generado:</div>
        <div class="text-negative text-h6">{{ registroGenerado }}</div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { buscarEquiposUtil } from 'src/utils/api_services'

const equipos = ref([])
const equipoSeleccionado = ref(null)
const software = ref('')
const estado = ref('')
const ticket = ref('')
const usuarioLic = ref('')
const registroGenerado = ref('')

const $q = useQuasar()

usuarioLic.value = localStorage.getItem('username')

// funcion para bloquear escritura en el select
function bloquearEscritura(e) {
  if (equipoSeleccionado.value && e.key !== 'Tab' && e.key !== 'Enter') {
    e.preventDefault()
  }
}

// función puente para el componente q-select
const buscarEquipos = (val, update) => {
  // Pasamos 'equipos' para que la utilidad sepa qué variable actualizar
  buscarEquiposUtil(val, update, equipos)
}

async function cargarLicencia() {
  if (!equipoSeleccionado.value) return
  const res = await api.get('busqueda/info_licencia/', {
    params: { equipo: equipoSeleccionado.value.nombre_equipo },
  })
  software.value = res.data.software
  estado.value = res.data.estado
}

async function recuperar() {
  // validación: Estado recuperada (Que ya lo tuviera)
  registroGenerado.value = equipoSeleccionado.value.estado // Limpiar registro previo
  if (estado.value === 'Recuperada' || estado.value === 'Trasladada') {
    registroGenerado.value = '-----'
    $q.notify({
      type: 'negative',
      message: 'Este equipo ya tiene una licencia recuperada o trasladada.',
    })
    return
  }

  // Validación de campos vacíos
  if (!equipoSeleccionado.value || !software.value || !ticket.value) {
    $q.notify({
      type: 'negative',
      message: 'Por favor, complete todos los campos antes de recuperar la licencia.',
    })
    return
  }

  try {
    ticket.value = String(ticket.value)
    await api.post('gestion_licencias/recuperar/', {
      nombre_equipo: equipoSeleccionado.value.nombre_equipo,
      software: software.value,
      ticket_retiro: ticket.value,
      usuario_licenciamiento: usuarioLic.value,
    })

    $q.notify({
      type: 'positive',
      message: 'Licencia recuperada',
    })
    // Generar la cadena de recuperación (-R-) antes de limpiar
    registroGenerado.value = equipoSeleccionado.value.estado //'-R-' + software.value + '-TK' + ticket.value + '-' + usuarioLic.value

    // Limpiar campos
    equipoSeleccionado.value = null
    software.value = ''
    ticket.value = ''
    usuarioLic.value = ''
  } catch (error) {
    console.error(error)
    $q.notify({
      type: 'negative',
      message: 'Error al recuperar la licencia',
    })
  }
}
</script>

<style scoped>
.asig-header {
  padding: 28px 32px;
  margin-bottom: 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, #00105b, #003399);
}

.asig-header__title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: white;
}

.asig-header__sub {
  margin-top: 8px;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  max-width: 700px;
}

.page-bg {
  background: #f5f6fa;
  padding: 32px;
}

.rounded-card {
  border-radius: 14px;
}

.shadow-card {
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.06);
}

.btn-action {
  border-radius: 10px;
  padding-left: 14px;
  padding-right: 14px;
  font-weight: 700;
}
</style>
