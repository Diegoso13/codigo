<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Traslado de licencia</div>

        <div class="asig-header__sub">
          Seleccione un equipo origen y destino para trasladar la licencia
        </div>
      </div>
    </div>

    <!-- FORM -->
    <q-card class="shadow-card rounded-card">
      <q-card-section>
        <div class="text-subtitle1 text-weight-bold q-mb-md">Datos de traslado</div>

        <div class="row q-col-gutter-md">
          <!-- EQUIPO ORIGEN -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="equipoOrigen"
              use-input
              input-debounce="300"
              label="Equipo origen"
              :options="equipos"
              option-label="nombre_equipo"
              @filter="buscarEquipos"
              @update:model-value="cargarLicencia"
              clearable
              @clear="((licencia = ''), (estado = ''))"
              @keydown="bloquearEscrituraOrigen"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="computer" />
              </template>
            </q-select>
          </div>

          <!-- EQUIPO DESTINO -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="equipoDestino"
              use-input
              input-debounce="300"
              label="Equipo destino"
              :options="equipos"
              option-label="nombre_equipo"
              @filter="buscarEquipos"
              clearable
              @clear="equipoDestino = null"
              @keydown="bloquearEscrituraDestino"
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
            <q-input v-model="licencia" label="Licencia" readonly outlined dense>
              <template #prepend>
                <q-icon name="vpn_key" />
              </template>
            </q-input>
          </div>

          <!-- ESTADO -->
          <div class="col-12 col-md-6">
            <q-input v-model="estado" label="Estado de licencia" readonly outlined dense>
              <template #prepend>
                <q-icon name="info" />
              </template>
            </q-input>
          </div>

          <!-- USUARIO DESTINO -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="usuarioDestino"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Usuario destino"
              :options="usuariosFiltrados"
              @filter="filtrarUsuarios"
            >
              <template #prepend>
                <q-icon name="person" />
              </template>
            </q-select>
          </div>

          <!-- TICKET -->
          <div class="col-12 col-md-6">
            <q-input
              v-model="ticket"
              label="Ticket traslado"
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

          <!-- MENSAJE DE ERROR -->
          <div
            v-if="
              equipoOrigen &&
              equipoDestino &&
              equipoOrigen.nombre_equipo === equipoDestino.nombre_equipo
            "
            class="col-12"
          >
            <q-banner class="bg-negative text-white rounded-borders">
              El equipo de origen y destino no pueden ser el mismo.
            </q-banner>
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- ACTIONS -->
      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          label="Realizar traslado"
          color="primary"
          unelevated
          class="btn-action"
          :disable="
            !equipoOrigen ||
            !equipoDestino ||
            !licencia ||
            !usuarioDestino ||
            !ticket ||
            equipoOrigen.nombre_equipo === equipoDestino.nombre_equipo
          "
          @click="trasladar"
        />
      </q-card-actions>
    </q-card>

    <!-- RESULTADO -->
    <q-card v-if="registroOrigen && registroDestino" class="shadow-card rounded-card q-mt-md">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <div class="text-weight-bold q-mb-sm">Para el equipo de origen:</div>
            <div class="text-negative text-h6">{{ registroOrigen }}</div>
          </div>
          <div class="col-12 col-md-6">
            <div class="text-weight-bold q-mb-sm">Para el equipo de destino:</div>
            <div class="text-primary text-h6">{{ registroDestino }}</div>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { buscarEquiposUtil } from 'src/utils/api_services'
import { useUsuarios } from 'src/composables/useUsuarios'

const equipos = ref([])
const equipoOrigen = ref(null)
const equipoDestino = ref(null)
const licencia = ref('')
const estado = ref('')
const usuarioDestino = ref('')
const usuariosFiltrados = ref([])
const ticket = ref('')
const usuarioLic = ref('')

const registroOrigen = ref('')
const registroDestino = ref('')

const $q = useQuasar()
const { usuarios, listar: listarUsuarios } = useUsuarios()

usuarioLic.value = localStorage.getItem('username')

// Funciones para bloquear escritura cuando ya hay selección (e definido para evitar error ESLint)
function bloquearEscrituraOrigen(e) {
  if (equipoOrigen.value && e.key !== 'Tab' && e.key !== 'Enter') {
    e.preventDefault()
  }
}

function bloquearEscrituraDestino(e) {
  if (equipoDestino.value && e.key !== 'Tab' && e.key !== 'Enter') {
    e.preventDefault()
  }
}

// función puente para el componente q-select
const buscarEquipos = (val, update) => {
  // Pasamos 'equipos' para que la utilidad sepa qué variable actualizar
  buscarEquiposUtil(val, update, equipos)
}

// Función para filtrar usuarios
async function filtrarUsuarios(val, update) {
  update(() => {
    usuariosFiltrados.value = []
  })

  await listarUsuarios({ search: val || '' })
  usuariosFiltrados.value = usuarios.value.map((u) => u.usuario)
}


async function cargarLicencia() {
  if (!equipoOrigen.value) return
  const res = await api.get('busqueda/info_licencia/', {
    params: { equipo: equipoOrigen.value.nombre_equipo },
  })
  licencia.value = res.data.software
  estado.value = res.data.estado
}

async function trasladar() {
  if (equipoOrigen.value.nombre_equipo === equipoDestino.value.nombre_equipo) {
    $q.notify({
      type: 'negative',
      message: 'El equipo de origen y destino no pueden ser el mismo.',
    })
    return
  }

  if (estado.value === 'Trasladada' || estado.value === '' || estado.value === 'Retirada') {
    $q.notify({
      type: 'negative',
      message: 'Este equipo no tiene licencia disponible.',
    })
    return
  }

  if (
    !equipoOrigen.value ||
    !equipoDestino.value ||
    !licencia.value ||
    !estado.value ||
    !usuarioDestino.value ||
    !ticket.value
  ) {
    $q.notify({
      type: 'negative',
      message: 'Por favor, complete todos los campos antes de realizar el traslado.',
    })
    return
  }

  try {
    ticket.value = String(ticket.value)
    await api.post('gestion_licencias/trasladar/', {
      equipo_origen: equipoOrigen.value.nombre_equipo,
      equipo_destino: equipoDestino.value.nombre_equipo,
      ticket: ticket.value,
      usuario_destino: usuarioDestino.value,
      usuario_licenciamiento: usuarioLic.value,
    })

    // 1. Generamos los textos
    registroOrigen.value = '-T-' + licencia.value + '-TK' + ticket.value + '-' + usuarioLic.value
    registroDestino.value = '-A-' + licencia.value + '-TK' + ticket.value + '-' + usuarioLic.value

    $q.notify({
      type: 'positive',
      message: 'Traslado realizado correctamente',
      icon: 'check',
    })

    // 2. Limpiamos los campos (el recuadro seguirá visible porque registroOrigen/Destino tienen datos)
    equipoOrigen.value = null
    equipoDestino.value = null
    licencia.value = ''
    usuarioDestino.value = ''
    ticket.value = ''
    usuarioLic.value = ''
  } catch (error) {
    console.error(error)
    $q.notify({
      type: 'negative',
      message: 'Error al realizar el traslado',
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
