<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Asignar licencia</div>

        <div class="asig-header__sub">
          Seleccione un equipo y complete los datos para asignar una licencia
        </div>
      </div>
    </div>

    <!-- FORM -->
    <q-card class="shadow-card rounded-card">
      <q-card-section>
        <div class="text-subtitle1 text-weight-bold q-mb-md">Datos de asignación</div>

        <div class="row q-col-gutter-md">
          <!-- EQUIPO -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="equipoSeleccionado"
              use-input
              input-debounce="300"
              label="Seleccionar equipo"
              :options="equipos"
              option-label="nombre_equipo"
              option-value="nombre_equipo"
              @filter="buscarEquipos"
              @update:model-value="cargarLicencia"
              clearable
              @keydown="bloquearEscritura"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="computer" />
              </template>
            </q-select>
          </div>

          <!-- USUARIO -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="usuario"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Usuario"
              :options="usuariosFiltrados"
              @filter="filtrarUsuarios"
            >
              <template #prepend>
                <q-icon name="person" />
              </template>
            </q-select>
          </div>

          <!-- SOFTWARE -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="software"
              option-label="nombre"
              option-value="nombre"
              emit-value
              map-options
              use-input
              fill-input
              hide-selected
              input-debounce="0"
              label="Software"
              :options="opcionesSoftware"
              @filter="filterSoftware"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="apps" />
              </template>
            </q-select>
          </div>

          <!-- PROPIETARIO -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="propietario"
              option-label="nombre"
              option-value="nombre"
              emit-value
              map-options
              use-input
              fill-input
              hide-selected
              input-debounce="0"
              label="Propietario"
              :options="opcionesPropietario"
              @filter="filterPropietario"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="business" />
              </template>
            </q-select>
          </div>

          <!-- SEDE -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="sede"
              option-label="nombre"
              option-value="nombre"
              emit-value
              map-options
              use-input
              fill-input
              hide-selected
              input-debounce="0"
              label="Sede"
              :options="opcionesSede"
              @filter="filterSede"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="location_on" />
              </template>
            </q-select>
          </div>

          <!-- CIUDAD -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="ciudad"
              option-label="nombre"
              option-value="nombre"
              emit-value
              map-options
              use-input
              fill-input
              hide-selected
              input-debounce="0"
              label="Ciudad"
              :options="opcionesCiudad"
              @filter="filterCiudad"
              outlined
              dense
            >
              <template #prepend>
                <q-icon name="public" />
              </template>
            </q-select>
          </div>

          <!-- TICKET -->
          <div class="col-12 col-md-6">
            <q-input
              v-model="ticket"
              label="Ticket asignación"
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
          label="Asignar licencia"
          color="primary"
          unelevated
          class="btn-action"
          :disable="
            !equipoSeleccionado ||
            !usuario ||
            !software ||
            !propietario ||
            !sede ||
            !ciudad ||
            !ticket
          "
          @click="asignar"
        />
      </q-card-actions>
    </q-card>

    <!-- RESULTADO -->
    <q-card v-if="registroGenerado" class="shadow-card rounded-card q-mt-md">
      <q-card-section>
        <div class="text-weight-bold q-mb-sm">Registro generado:</div>
        <div class="text-primary text-h6">{{ registroGenerado }}</div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { buscarEquiposUtil } from 'src/utils/api_services'
import { useUsuarios } from 'src/composables/useUsuarios'
import {
  obtenerSoftware,
  obtenerSedes,
  obtenerCiudades,
  obtenerPropietarios,
} from 'src/services/CatalogosLicencias'

const equipos = ref([])
const equipoSeleccionado = ref(null)

const usuario = ref('')
const usuariosFiltrados = ref([])
const software = ref('')
const propietario = ref('')
const sede = ref('')
const ciudad = ref('')
const ticket = ref('')
const estado = ref('')
const usuarioLic = ref('')
const registroGenerado = ref('')

const { usuarios, listar: listarUsuarios } = useUsuarios()

usuarioLic.value = localStorage.getItem('username')

const $q = useQuasar()

async function cargarCatalogo(servicio, listaRef, opcionesRef) {
  try {
    const data = await servicio()

    listaRef.value = data
    opcionesRef.value = data
  } catch (error) {
    console.error(error)

    $q.notify({
      type: 'negative',
      message: 'Error cargando catálogo',
    })
  }
}

onMounted(async () => {
  await cargarCatalogo(obtenerSoftware, listaSoftware, opcionesSoftware)
  await cargarCatalogo(obtenerSedes, listaSedes, opcionesSede)
  await cargarCatalogo(obtenerCiudades, listaCiudades, opcionesCiudad)
  await cargarCatalogo(obtenerPropietarios, listaPropietarios, opcionesPropietario)
})

// Listas de ejemplo
//const listaSoftware = ['Office 2016 std', 'Office 2019 std', 'Office 2021 std']
//const listaPropietarios = ['Emtelco', 'Andirent', 'Compurent', 'Comfama']
//const listaSedes = ['Olaya', 'Aguacatala', 'El dorado']
//const listaCiudades = ['Medellín', 'Bogotá']
const listaSoftware = ref([])
const listaPropietarios = ref([])
const listaSedes = ref([])
const listaCiudades = ref([])

//const opcionesSoftware = ref(listaSoftware)
//const opcionesPropietario = ref(listaPropietarios)
//const opcionesSede = ref(listaSedes)
//const opcionesCiudad = ref(listaCiudades)
const opcionesSoftware = ref([])
const opcionesPropietario = ref([])
const opcionesSede = ref([])
const opcionesCiudad = ref([])

// Lógica de filtrado genérica
// function filtrar(val, update, lista, refOpciones) {
//   update(() => {
//     const needle = val.toLowerCase()
//     refOpciones.value = lista.filter((v) => v.toLowerCase().indexOf(needle) > -1)
//   })
// }

//const filterSoftware = (val, update) => filtrar(val, update, listaSoftware, opcionesSoftware)
//const filterPropietario = (val, update) => filtrar(val, update, listaPropietarios, opcionesPropietario)
//const filterSede = (val, update) => filtrar(val, update, listaSedes, opcionesSede)
//const filterCiudad = (val, update) => filtrar(val, update, listaCiudades, opcionesCiudad)
const filterSoftware = (val, update) => {
  update(() => {
    const needle = val.toLowerCase()

    opcionesSoftware.value = listaSoftware.value.filter((v) =>
      v.nombre.toLowerCase().includes(needle),
    )
  })
}

const filterPropietario = (val, update) => {
  update(() => {
    const needle = val.toLowerCase()

    opcionesPropietario.value = listaPropietarios.value.filter((v) =>
      v.nombre.toLowerCase().includes(needle),
    )
  })
}

const filterSede = (val, update) => {
  update(() => {
    const needle = val.toLowerCase()

    opcionesSede.value = listaSedes.value.filter((v) => v.nombre.toLowerCase().includes(needle))
  })
}

const filterCiudad = (val, update) => {
  update(() => {
    const needle = val.toLowerCase()

    opcionesCiudad.value = listaCiudades.value.filter((v) =>
      v.nombre.toLowerCase().includes(needle),
    )
  })
}

// funcion para bloquear escritura en el select
function bloquearEscritura(e) {
  if (equipoSeleccionado.value && e.key !== 'Tab' && e.key !== 'Enter') {
    e.preventDefault()
  }
}

// Función para filtrar usuarios
async function filtrarUsuarios(val, update) {
  update(() => {
    usuariosFiltrados.value = []
  })

  await listarUsuarios({ search: val || '' })
  usuariosFiltrados.value = usuarios.value.map((u) => u.usuario)
}

// función puente para el componente q-select
const buscarEquipos = (val, update) => {
  // Pasamos 'equipos' para que la utilidad sepa qué variable actualizar
  buscarEquiposUtil(val, update, equipos)
}

// Se llama cada vez que para verificar el estado de la licencia del equipo seleccionado y ver si tiene alguna asignada
async function cargarLicencia() {
  if (!equipoSeleccionado.value) return
  const res = await api.get('busqueda/info_licencia/', {
    params: { equipo: equipoSeleccionado.value.nombre_equipo },
  })
  estado.value = res.data.estado
}

async function asignar() {
  // Validación de campos
  if (
    !equipoSeleccionado.value ||
    !usuario.value ||
    !software.value ||
    !propietario.value ||
    !sede.value ||
    !ciudad.value ||
    !ticket.value
  ) {
    $q.notify({
      type: 'negative',
      message: 'Por favor, complete todos los campos antes de asignar la licencia.',
    })
  }

  if (estado.value === 'Asignada') {
    $q.notify({
      type: 'negative',
      message: 'Este equipo ya tiene una licencia asignada.',
    })
    return
  }

  try {
    ticket.value = String(ticket.value)
    await api.post('gestion_licencias/asignar/', {
      nombre_equipo: equipoSeleccionado.value.nombre_equipo,
      usuario: usuario.value,
      software: software.value,
      propietario: propietario.value,
      sede: sede.value,
      ciudad: ciudad.value,
      ticket_asignacion: ticket.value,
      usuario_licenciamiento: usuarioLic.value,
    })

    registroGenerado.value = '-A-' + software.value + '-TK' + ticket.value + '-' + usuarioLic.value
    $q.notify({
      type: 'positive',
      message: 'Licencia asignada correctamente',
      icon: 'check',
    })

    equipoSeleccionado.value = null
    usuario.value = ''
    software.value = ''
    propietario.value = ''
    sede.value = ''
    ciudad.value = ''
    ticket.value = ''
    usuarioLic.value = ''
  } catch (error) {
    console.error(error)
    $q.notify({
      type: 'negative',
      message: 'Error al asignar licencia',
      icon: 'report_problem',
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
