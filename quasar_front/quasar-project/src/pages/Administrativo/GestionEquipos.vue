<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Gestión de Equipos</div>

        <div class="asig-header__sub">
          Agregue nuevos equipos o edite los datos de equipos existentes
        </div>
      </div>
    </div>

    <!-- FORMULARIOS -->
    <div class="row q-col-gutter-md">
      <!-- AGREGAR EQUIPO -->
      <div class="col-12 col-md-6">
        <q-card class="shadow-card rounded-card">
          <q-card-section>
            <div class="text-subtitle1 text-weight-bold q-mb-md">Agregar equipo</div>

            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-12 col-sm-5">
                <q-select
                  v-model="prefijo_creacion"
                  :options="opcionesprefijo_creacion"
                  label="Sede/Tipo"
                  outlined
                  dense
                >
                  <template #prepend>
                    <q-icon name="business" />
                  </template>
                </q-select>
              </div>
              <div class="col-12 col-sm-7">
                <q-input
                  v-model="numeroPlaca"
                  label="Número de placa"
                  outlined
                  dense
                  type="number"
                  class="no-spinner"
                >
                  <template #prepend>
                    <q-icon name="tag" />
                  </template>
                </q-input>
              </div>
            </div>

            <q-input
              v-model="serial_creacion"
              label="Serial del equipo"
              outlined
              dense
              @keypress="bloquearEspeciales"
              @update:model-value="
                (val) => (serial_creacion = val.toUpperCase().replace(/[^A-Z0-9]/g, ''))
              "
            >
              <template #prepend>
                <q-icon name="fingerprint" />
              </template>
            </q-input>
          </q-card-section>

          <q-separator />

          <q-card-actions align="right" class="q-pa-md">
            <q-btn
              :disable="!numeroPlaca"
              label="Agregar equipo"
              color="primary"
              unelevated
              class="btn-action"
              @click="validarYAgregar"
            />
          </q-card-actions>
        </q-card>
      </div>

      <!-- EDITAR EQUIPO -->
      <div class="col-12 col-md-6">
        <q-card class="shadow-card rounded-card">
          <q-card-section>
            <div class="text-subtitle1 text-weight-bold q-mb-md">Editar equipo</div>

            <q-select
              v-model="equipoSeleccionado"
              use-input
              input-debounce="300"
              label="Seleccionar equipo a editar"
              :options="equipos"
              option-label="nombre_equipo"
              option-value="nombre_equipo"
              @filter="buscarEquipos"
              clearable
              @keydown="bloquearEscritura"
              outlined
              dense
              class="q-mb-md"
            >
              <template #prepend>
                <q-icon name="computer" />
              </template>
            </q-select>

            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-12 col-sm-5">
                <q-select
                  v-model="prefijo_edicion"
                  :options="opcionesprefijo_edicion"
                  label="Sede/Tipo"
                  outlined
                  dense
                >
                  <template #prepend>
                    <q-icon name="business" />
                  </template>
                </q-select>
              </div>
              <div class="col-12 col-sm-7">
                <q-input
                  v-model="nuevo_numeroPlaca"
                  label="Número de placa"
                  outlined
                  dense
                  type="number"
                  class="no-spinner"
                >
                  <template #prepend>
                    <q-icon name="tag" />
                  </template>
                </q-input>
              </div>
            </div>

            <q-input
              v-model="serial_edicion"
              label="Serial del equipo"
              outlined
              dense
              @keypress="bloquearEspeciales"
              @update:model-value="
                (val) => (serial_edicion = val.toUpperCase().replace(/[^A-Z0-9]/g, ''))
              "
            >
              <template #prepend>
                <q-icon name="fingerprint" />
              </template>
            </q-input>
          </q-card-section>

          <q-separator />

          <q-card-actions align="right" class="q-pa-md">
            <q-btn
              :disable="!nuevo_numeroPlaca"
              label="Actualizar datos"
              color="primary"
              unelevated
              class="btn-action"
              @click="editarEquipo"
            />
          </q-card-actions>
        </q-card>
      </div>
    </div>

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
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { buscarEquiposUtil } from 'src/utils/api_services'
const $q = useQuasar()

// Refs para Agregar
const prefijo_creacion = ref('PORTADM')
const numeroPlaca = ref('')
const serial_creacion = ref('')
const registroGenerado = ref('')
const opcionesprefijo_creacion = [
  'prueba',
  'PORTADM',
  'OL',
  'ED',
  'BG',
  'ME',
  'IR_PREMISA',
  'PR_PREMISA',
]

// Refs para Editar
const prefijo_edicion = ref('PORTADM')
const equipoSeleccionado = ref(null)
const serial_edicion = ref('')
const nuevo_numeroPlaca = ref('')
const equipos = ref([])
const opcionesprefijo_edicion = [
  'prueba',
  'PORTADM',
  'OL',
  'ED',
  'BG',
  'ME',
  'IR_PREMISA',
  'PR_PREMISA',
]

/* =========================
   BÚSQUEDA GENÉRICA
========================= */
// función puente para el componente q-select
const buscarEquipos = (val, update) => {
  // Pasamos 'equipos' para que la utilidad sepa qué variable actualizar
  buscarEquiposUtil(val, update, equipos)
}

// funcion para bloquear escritura en el select
function bloquearEscritura(e) {
  if (equipoSeleccionado.value && e.key !== 'Tab' && e.key !== 'Enter') {
    e.preventDefault()
  }
}

// funcion para bloquear caracteres especiales en el input de serial
function bloquearEspeciales(e) {
  // Permitir solo letras (A-Z, a-z) y números (0-9)
  // La regex [a-zA-Z0-9] verifica si la tecla presionada es válida
  const regex = new RegExp('^[a-zA-Z0-9]+$')
  const key = String.fromCharCode(!e.charCode ? e.which : e.charCode)

  // Si la tecla no coincide con la regex, cancelamos el evento
  if (!regex.test(key)) {
    e.preventDefault()
    return false
  }
}

/* =========================
   AGREGAR EQUIPO
========================= */

async function validarYAgregar() {
  // 1. Validar campos vacíos
  if (!prefijo_creacion.value || !numeroPlaca.value || !serial_creacion.value) {
    $q.notify({ type: 'negative', message: 'Debe completar todos los campos' })
    return
  }

  // 2. Construir el nombre completo (Concatenar con "-")
  const nombreCompleto = `${prefijo_creacion.value}-${numeroPlaca.value}`.replace(/\s+/g, '')

  try {
    // 3. Verificar si el equipo ya existe usando la API de búsqueda
    const checkExist = await api.get('busqueda/select/', {
      params: { q: nombreCompleto },
    })

    // Si la búsqueda devuelve un equipo con el nombre exacto, bloqueamos
    const existe = checkExist.data.some(
      (e) => e.nombre_equipo.toUpperCase() === nombreCompleto.toUpperCase(),
    )

    if (existe) {
      $q.notify({
        type: 'negative',
        message: `El equipo ${nombreCompleto} ya se encuentra creado.`,
        icon: 'warning',
      })
      return
    }

    // 4. Si no existe, procedemos a agregar
    const res = await api.post('edicion_equipos/', {
      nombre_equipo: nombreCompleto,
      serial: serial_creacion.value,
    })

    registroGenerado.value = nombreCompleto + '  -  ' + serial_creacion.value
    $q.notify({ type: 'positive', message: res.data.mensaje || 'Equipo agregado con éxito' })

    // Limpiar campos
    numeroPlaca.value = ''
    serial_creacion.value = ''
  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Error al procesar la operación' })
  }
}

/* =========================
   EDITAR EQUIPO
========================= */

async function editarEquipo() {
  if (!equipoSeleccionado.value || !nuevo_numeroPlaca.value) {
    $q.notify({ type: 'negative', message: 'Debe completar los campos de edición' })
    return
  }

  const nombreCompleto = `${prefijo_edicion.value}-${nuevo_numeroPlaca.value}`.replace(/\s+/g, '')

  const checkExist = await api.get('busqueda/select/', {
    params: { q: nombreCompleto },
  })

  // Si la búsqueda devuelve un equipo con el nombre exacto, bloqueamos
  const existe = checkExist.data.some(
    (e) => e.nombre_equipo.toUpperCase() === nombreCompleto.toUpperCase(),
  )

  if (existe) {
    $q.notify({
      type: 'negative',
      message: 'Los datos corresponden a un equipo ya existente',
      icon: 'warning',
    })
    return
  }

  try {
    const res = await api.post('edicion_equipos/editar_nombre/', {
      nombre_actual: equipoSeleccionado.value.nombre_equipo,
      nombre_nuevo: nombreCompleto,
      serial_nuevo: serial_edicion.value,
    })

    $q.notify({ type: 'positive', message: res.data.mensaje })

    equipoSeleccionado.value = null
    nuevo_numeroPlaca.value = ''
  } catch (error) {
    console.error(error)
    $q.notify({ type: 'negative', message: 'Error al editar equipo' })
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
