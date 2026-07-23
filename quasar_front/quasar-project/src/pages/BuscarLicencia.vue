<template>
  <q-page class="ext-page">
    <!-- HEADER -->
    <div class="ext-header">
      <div>
        <div class="ext-header__title">Búsqueda de Equipos</div>

        <div class="ext-header__sub">{{ resultados.length }} registros encontrados</div>
      </div>

      <div class="ext-header__actions">
        <q-btn
          v-if="['licenciamiento', 'admin'].includes(rol)"
          color="green"
          icon="download"
          label="Exportar"
          :loading="cargando"
          @click="exportarBaseDatosCompleta"
          unelevated
        />
      </div>
    </div>

    <!-- FILTROS -->
    <q-card flat bordered class="q-mx-lg q-mt-md q-mb-md">
      <q-card-section>
        <div class="ext-filters">
          <div class="ext-filters__top">
            <q-select
              v-model="busqueda"
              use-input
              input-debounce="300"
              label="Buscar equipo en base de datos..."
              :options="equipos"
              option-label="nombre_equipo"
              @filter="buscarEquipos"
              clearable
              outlined
              dense
              options-dense
              @keydown="bloquearEscrituraOrigen"
              class="ext-filters__select"
            >
              <template v-slot:prepend>
                <q-icon name="devices" size="18px" />
              </template>
            </q-select>

            <q-btn
              label="Buscar"
              color="primary"
              icon="search"
              unelevated
              class="ext-filters__button"
              @click="buscar"
              :loading="cargando"
            />
          </div>

          <div class="ext-filters__bottom">
            <q-input
              outlined
              dense
              debounce="300"
              v-model="filtroTabla"
              placeholder="Filtrar resultados actuales..."
              class="ext-filters__search"
            >
              <template v-slot:prepend>
                <q-icon name="search" size="18px" />
              </template>

              <template v-slot:append v-if="filtroTabla">
                <q-icon
                  name="close"
                  size="16px"
                  class="cursor-pointer"
                  @click="filtroTabla = ''"
                />
              </template>
            </q-input>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <!-- TABLA -->
    <q-card flat bordered class="q-mx-lg q-mb-lg">
      <q-card-section>
        <q-table
          :table-header-style="{
            background: '#00105b',
            color: 'white',
          }"
          :rows="resultados"
          :columns="columns_cond"
          row-key="id"
          :filter="filtroTabla"
          :loading="cargando"
          v-model:pagination="pagination"
          flat
          bordered
          no-data-label="Sin equipos."
          class="ext-table"
        >
          <template #loading>
            <q-inner-loading showing>
              <q-spinner-dots size="40px" color="primary" />
            </q-inner-loading>
          </template>

          <template v-slot:no-data>
            <div class="full-width column flex-center q-pa-lg text-grey-6">
              <q-icon name="search_off" size="36px" class="text-grey-4" />
              <div class="text-body2 text-weight-medium q-mt-xs">
                No se encontraron equipos coincidentes
              </div>
            </div>
          </template>

          <template v-slot:body-cell-estado="props">
            <q-td :props="props">
              <span class="ext-chip">
                {{ props.row.estado || '---' }}
              </span>
            </q-td>
          </template>

          <template v-slot:body-cell-detalles="props">
            <q-td
              v-if="['licenciamiento', 'admin'].includes(rol)"
              :props="props"
              class="text-center"
            >
              <q-btn
                flat
                round
                color="primary"
                icon="visibility"
                size="sm"
                @click="verDetalles(props.row)"
              >
                <q-tooltip class="bg-dark text-white shadow-2 text-caption">Ver detalles</q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <q-dialog
      v-model="showDetails"
      v-if="['licenciamiento', 'admin'].includes(rol)"
      transition-show="scale"
      transition-hide="scale"
    >
      <q-card class="details-dialog">
        <q-card-section class="details-dialog__header row items-center q-py-sm">
          <div class="column">
            <div class="text-subtitle1 text-weight-bold">{{ selectedItem.nombre_equipo }}</div>
          </div>
          <q-space />
          <q-btn icon="close" flat round dense size="sm" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-md scroll" style="max-height: 65vh">
          <div class="row q-col-gutter-sm">
            <div v-for="(val, key) in selectedItem" :key="key" class="col-12 col-sm-6">
              <div class="detail-card q-pa-sm">
                <div class="detail-card__label">
                  {{ key.replace(/_/g, ' ') }}
                </div>
                <div class="detail-card__value">
                  {{ val || '---' }}
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from 'boot/axios'
import { exportFile, useQuasar } from 'quasar'
import { buscarEquiposUtil } from 'src/utils/api_services'

const $q = useQuasar()
const busqueda = ref(null)
const equipos = ref([])
const resultados = ref([])
const buscado = ref(false)
const cargando = ref(false)
const filtroTabla = ref('')
const rol = ref('')
const showDetails = ref(false)
const selectedItem = ref({})

const pagination = ref({
  rowsPerPage: 10,
})

const allColumns = [
  { name: 'nombre_equipo', label: 'Equipo', field: 'nombre_equipo', align: 'left', sortable: true },
  { name: 'serial', label: 'Serial', field: 'serial', align: 'left', sortable: true },
  { name: 'software', label: 'Software', field: 'software', align: 'left', sortable: true },
  {
    name: 'usuario',
    label: 'Usuario',
    field: (row) => row.usuario || 'Sin asignar',
    align: 'left',
    sortable: true,
  },
  { name: 'estado', label: 'Estado', field: 'estado', align: 'center' },
  { name: 'fecha', label: 'Fecha', field: 'fecha', align: 'left', sortable: true },
  { name: 'detalles', label: 'Detalles', field: 'detalles', align: 'center' },
]

onMounted(async () => {
  rol.value = localStorage.getItem('rol') || ''
  await cargarTodosEquipos()
})

async function cargarTodosEquipos() {
  try {
    cargando.value = true
    const response = await api.get('busqueda/busqueda/', { params: { q: '' } })
    resultados.value = response.data
  } catch (err) {
    console.error(err)
    if (err.response?.status === 403) {
      $q.notify({ type: 'negative', message: 'No tienes permisos (Rol insuficiente)' })
    } else {
      $q.notify({ type: 'negative', message: 'Error al cargar los equipos' })
    }
  } finally {
    cargando.value = false
  }
}

function bloquearEscrituraOrigen(e) {
  if (busqueda.value && e.key !== 'Tab' && e.key !== 'Enter') {
    e.preventDefault()
  }
}

const columns_cond = computed(() => {
  const rolesPermitidos = ['licenciamiento', 'admin']
  if (rolesPermitidos.includes(rol.value)) {
    return allColumns
  }
  return allColumns.filter((col) => col.name !== 'detalles')
})

const buscarEquipos = (val, update) => {
  buscarEquiposUtil(val, update, equipos)
}

async function buscar() {
  const termino =
    typeof busqueda.value === 'object' && busqueda.value !== null
      ? busqueda.value.nombre_equipo
      : busqueda.value

  if (!termino) {
    await cargarTodosEquipos()
    return
  }

  cargando.value = true
  try {
    const response = await api.get('busqueda/busqueda/', { params: { q: termino } })
    resultados.value = response.data
    buscado.value = true
  } catch (err) {
    console.error(err)
    if (err.response?.status === 403) {
      $q.notify({ type: 'negative', message: 'No tienes permisos (Rol insuficiente)' })
    }
  } finally {
    cargando.value = false
  }
}

function verDetalles(item) {
  selectedItem.value = item
  showDetails.value = true
}

async function exportarBaseDatosCompleta() {
  try {
    $q.loading.show({ message: 'Preparando descarga...' })
    const response = await api.get('busqueda/exportar/', { params: { q: '' } })
    const datos = response.data
    if (datos.length === 0) {
      $q.notify({ type: 'warning', message: 'No hay datos para exportar' })
      return
    }
    const columnasCsv = Object.keys(datos[0])
    const csvContent = [
      columnasCsv.join(';'),
      ...datos.map((row) =>
        columnasCsv.map((col) => String(row[col] || '').replace(/;/g, ' ')).join(';'),
      ),
    ].join('\r\n')
    exportFile('inventario_total.csv', '\ufeff' + csvContent, 'text/csv')
  } catch (err) {
    console.error(err)
    $q.notify({ type: 'negative', message: 'Error de permisos al exportar' })
  } finally {
    $q.loading.hide()
  }
}
</script>

<style scoped>
.ext-page {
  background: #f0f2f7;
  min-height: 100vh;
}

.ext-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px;
  margin: 0 24px;
  margin-top: 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, #00105b, #003399);
}

.ext-header__title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: white;
}

.ext-header__sub {
  margin-top: 6px;
  color: rgba(255, 255, 255, 0.85);
}

.ext-header__actions {
  display: flex;
  align-items: center;
}

.ext-filters {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.ext-filters__top {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}

.ext-filters__bottom {
  display: flex;
  justify-content: center;
}

.ext-filters__select,
.ext-filters__search {
  width: 100%;
  max-width: 650px;
}

.ext-filters__button {
  min-width: 130px;
}

.ext-table :deep(.q-table th) {
  font-weight: 700;
}

.ext-table :deep(.q-table td) {
  vertical-align: middle;
}

.ext-table :deep(tbody tr:nth-child(even)) {
  background-color: #f7f9fc;
}

.ext-table :deep(tbody tr:hover) {
  background-color: #eef4ff;
}

.ext-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  background: #e8f0fe;
  color: #1a56c4;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}

.details-dialog {
  width: 600px;
  max-width: 90vw;
  border-radius: 8px;
}

.details-dialog__header {
  color: white;
  background: linear-gradient(135deg, #00105b, #003399);
}

.detail-card {
  height: 100%;
  border-left: 2px solid #00105b;
  border-radius: 6px;
  background: #f4f6fb;
}

.detail-card__label {
  font-size: 10px;
  font-weight: 800;
  color: #00105b;
  text-transform: uppercase;
}

.detail-card__value {
  color: #1f2937;
  font-size: 12px;
  font-weight: 500;
  overflow-wrap: anywhere;
  white-space: normal;
}

@media (max-width: 600px) {
  .ext-header {
    margin: 12px;
    padding: 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .ext-header__title {
    font-size: 1.55rem;
  }

  .ext-header__actions,
  .ext-header__actions .q-btn,
  .ext-filters__button {
    width: 100%;
  }
}
</style>
