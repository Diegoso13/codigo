<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Liberar extensión</div>

        <div class="asig-header__sub">
          Seleccione una extensión para liberarla si esta en estado de CREADA
        </div>
      </div>
    </div>

    <!-- FORM -->
    <q-card class="shadow-card rounded-card">
      <q-card-section>
        <div class="text-subtitle1 text-weight-bold q-mb-sm">Datos de liberación</div>

        <div class="row q-col-gutter-md">
          <!-- EXTENSION -->
          <div class="col-12 col-md-6">
            <q-select
              v-model="form.extension"
              outlined
              dense
              use-input
              input-debounce="200"
              clearable
              label="Extensión"
              :options="extensionesCreadasFiltradas"
              @filter="filtrarExtensiones"
              :disable="loading"
              :error="!!errores.extension"
              :error-message="errores.extension"
            >
              <template #prepend>
                <q-icon name="dialpad" />
              </template>
            </q-select>
          </div>

          <!-- TICKET -->
          <div class="col-12 col-md-6">
            <q-input
              v-model="form.ticket_eliminacion"
              outlined
              dense
              label="Ticket de liberación"
              :disable="loading"
              :error="!!errores.ticket_eliminacion"
              :error-message="errores.ticket_eliminacion"
            />
          </div>

          <!-- OBSERVACION -->
          <div class="col-12">
            <q-input
              v-model="form.observacion"
              outlined
              dense
              type="textarea"
              autogrow
              label="Observación"
              :disable="loading"
            />
          </div>
        </div>
      </q-card-section>

      <q-separator />

      <!-- ACTIONS -->
      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          color="primary"
          label="Liberar extensión"
          unelevated
          class="btn-action"
          :loading="loading"
          @click="liberarExtension"
        />
      </q-card-actions>
    </q-card>

    <q-dialog v-model="showMovDialog">
      <q-card style="min-width: 1200px">
        <q-card-section class="text-h6"> Movimientos generados </q-card-section>

        <q-separator />

        <q-card-section>
          <q-table
            :rows="movimientoActual ? [movimientoActual] : []"
            :columns="columnasMovimiento"
            row-key="id"
            dense
            flat
            hide-pagination
          />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn color="primary" label="Aceptar" @click="cerrarDialog" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useExtensiones } from 'src/composables/useExtensiones'

const router = useRouter()

const { extensiones, loading, listar, liberar } = useExtensiones()

const form = ref({
  extension: '',
  ticket_eliminacion: '',
  observacion: '',
})

const errores = ref({
  extension: '',
  ticket_eliminacion: '',
})

const extensionesCreadasFiltradas = ref([])

async function cargarExtensionesCreadas() {
  await listar({ estado: 'CREADA' })
  extensionesCreadasFiltradas.value = extensiones.value.map((e) => e.extension)
}

function filtrarExtensiones(val, update) {
  update(() => {
    const needle = val.toLowerCase()

    extensionesCreadasFiltradas.value = extensiones.value
      .map((e) => e.extension)
      .filter((ext) => ext.toLowerCase().includes(needle))
  })
}

onMounted(async () => {
  await cargarExtensionesCreadas()
})

function validar() {
  errores.value.extension = ''
  errores.value.ticket_eliminacion = ''

  if (!form.value.extension.trim()) {
    errores.value.extension = 'La extensión es obligatoria.'
    return false
  }

  if (!form.value.ticket_eliminacion.trim()) {
    errores.value.ticket_eliminacion = 'El ticket de liberación es obligatorio.'
    return false
  }

  return true
}

function limpiar() {
  form.value.extension = ''
  form.value.ticket_eliminacion = ''
  form.value.observacion = ''

  errores.value.extension = ''
  errores.value.ticket_eliminacion = ''
}

async function liberarExtension() {
  if (!validar()) return

  const res = await liberar({
    extension: form.value.extension.trim(),
    ticket_eliminacion: form.value.ticket_eliminacion.trim(),
    observacion: form.value.observacion.trim(),
  })

  movimientoActual.value = res?.movimientos?.[0] || res?.movimiento || null

  showMovDialog.value = true

  limpiar()
}

///mostrar movimiento

function cerrarDialog() {
  showMovDialog.value = false
  router.push('/extensiones')
}

const showMovDialog = ref(false)
const movimientoActual = ref(null)

const columnasMovimiento = [
  { name: 'extension', label: 'Extensión', field: 'extension', align: 'left' },
  { name: 'cliente', label: 'Cliente', field: 'cliente', align: 'left' },
  { name: 'direccion', label: 'Dirección', field: 'direccion', align: 'left' },
  { name: 'tipo', label: 'Tipo', field: 'tipo', align: 'left' },
  { name: 'division', label: 'División', field: 'division', align: 'left' },
  { name: 'plataforma', label: 'Plataforma', field: 'plataforma', align: 'left' },
  { name: 'cedula', label: 'Cedula', field: 'cedula', align: 'left' },
  { name: 'usuario', label: 'Usuario', field: 'usuario', align: 'left' },
  { name: 'cargo', label: 'Cargo', field: 'cargo', align: 'left' },
  { name: 'marca', label: 'Marca', field: 'marca', align: 'left' },
]
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
