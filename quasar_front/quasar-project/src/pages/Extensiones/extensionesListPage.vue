<template>
  <q-page class="ext-page">
    <!-- HEADER -->
    <div class="ext-header">
      <div>
        <div class="ext-header__title">Extensiones</div>

        <div class="ext-header__sub">{{ extensiones.length }} registros encontrados</div>
      </div>

      <div class="ext-header__actions">
        <q-btn
          color="green"
          icon="download"
          label="Exportar"
          :loading="loading"
          @click="exportar"
          unelevated
        />
      </div>
    </div>

    <!-- FILTROS -->
    <q-card flat bordered class="q-mx-lg q-mt-md q-mb-md">
      <q-card-section>
        <div class="ext-filters">
          <!-- TIPO ARRIBA CENTRADO -->
          <div class="ext-filters__top">
            <q-btn-toggle
              v-model="filtros.tipo"
              toggle-color="primary"
              unelevated
              rounded
              dense
              :options="[
                { label: 'Todos', value: null },
                { label: 'Operación', value: 'Operación' },
                { label: 'Administrativa', value: 'Administrativa' },
              ]"
            />
          </div>

          <!-- FILTROS ABAJO -->
          <div class="ext-filters__bottom">
            <q-input
              v-model="filtros.search"
              outlined
              dense
              debounce="0"
              placeholder="Buscar por extensión, cliente, usuario, cédula"
              class="ext-filters__search"
            >
              <template #prepend>
                <q-icon name="search" size="18px" />
              </template>

              <template #append>
                <q-icon
                  v-if="filtros.search"
                  name="close"
                  size="16px"
                  class="cursor-pointer"
                  @click="filtros.search = ''"
                />
              </template>
            </q-input>

            <q-select
              v-model="filtros.estado"
              :options="['DISPONIBLE', 'CREADA', 'ELIMINADA', 'DESACTIVADA']"
              outlined
              dense
              clearable
              placeholder="Estado"
              class="ext-filters__estado"
            />
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
          :rows="extensiones"
          :columns="columnas"
          row-key="extension"
          flat
          :loading="loading"
          :pagination="{ rowsPerPage: 10 }"
          no-data-label="Sin extensiones."
          class="ext-table"
        >
          <template #loading>
            <q-inner-loading showing>
              <q-spinner-dots size="40px" color="primary" />
            </q-inner-loading>
          </template>

          <template #body-cell-estado="props">
            <q-td :props="props">
              <span :class="chipClass(props.row.estado)">
                {{ props.row.estado }}
              </span>
            </q-td>
          </template>

          <template #body-cell-fecha_ultima_modificacion="props">
            <q-td :props="props">
              {{ formatFecha(props.row.fecha_ultima_modificacion) }}
            </q-td>
          </template>

          <template #body-cell-ticket_eliminacion="props">
            <q-td :props="props">
              {{ props.row.ticket_eliminacion || '—' }}
            </q-td>
          </template>

          <template #body-cell-observacion="props">
            <q-td :props="props">
              <span class="ext-obs" :title="props.row.observacion">
                {{ props.row.observacion || '—' }}
              </span>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useExtensiones } from 'src/composables/useExtensiones'

const { extensiones, loading, filtros, listar, buscarConDebounce, exportar } = useExtensiones()

onMounted(() => {
  listar()
})

watch(
  () => filtros.value.search,
  () => buscarConDebounce(),
)

watch(
  () => [filtros.value.estado, filtros.value.tipo],
  () => listar(),
)

// ─── Columnas ─────────────────────────────────────────────────
const columnas = [
  { name: 'extension', label: 'Extensión', field: 'extension', align: 'left', sortable: true },
  { name: 'estado', label: 'Estado', field: 'estado', align: 'left', sortable: true },
  { name: 'cliente', label: 'Cliente', field: 'cliente', align: 'left', sortable: true },
  { name: 'direccion', label: 'Direccion', field: 'direccion', align: 'left', sortable: true },
  { name: 'tipo', label: 'Tipo', field: 'tipo', align: 'left' },
  { name: 'division', label: 'División', field: 'division', align: 'left' },
  { name: 'campana', label: 'Campaña', field: 'campana', align: 'left' },
  { name: 'codigoceco', label: 'Cod.Ceco', field: 'codigoceco', align: 'left' },
  { name: 'ceco', label: 'Ceco', field: 'ceco', align: 'left' },
  { name: 'cliente2', label: 'Cliente 2', field: 'cliente2', align: 'left' },
  { name: 'plataforma', label: 'Plataforma', field: 'plataforma', align: 'left' },
  { name: 'cedula', label: 'Cédula', field: 'cedula', align: 'left' },
  { name: 'usuario', label: 'Usuario', field: 'usuario', align: 'left' },
  { name: 'puesto_trabajo', label: 'Puesto de trabajo', field: 'puesto_trabajo', align: 'left' },
  { name: 'sede', label: 'Sede', field: 'sede', align: 'left' },
  { name: 'cargo', label: 'Cargo', field: 'cargo', align: 'left' },
  {
    name: 'fecha_ultima_modificacion',
    label: 'Última modificación',
    field: 'fecha_ultima_modificacion',
    align: 'left',
  },
  { name: 'ticket_solicitud', label: 'Ticket solicitud', field: 'ticket_solicitud', align: 'left' },
  {
    name: 'ticket_eliminacion',
    label: 'Ticket eliminación',
    field: 'ticket_eliminacion',
    align: 'left',
  },
  { name: 'observacion', label: 'Observación', field: 'observacion', align: 'left' },
]

// ─── Helpers ──────────────────────────────────────────────────
function chipClass(estado) {
  const base = 'ext-chip'
  const map = {
    DISPONIBLE: 'ext-chip--disponible',
    CREADA: 'ext-chip--creada',
    ELIMINADA: 'ext-chip--eliminada',
  }
  return `${base} ${map[estado] ?? ''}`
}

function formatFecha(val) {
  if (!val) return '—'

  // Si viene como "YYYY-MM-DD", parsear manualmente
  const parts = val.split('-')
  if (parts.length === 3) {
    const [year, month, day] = parts.map(Number)
    const d = new Date(year, month - 1, day) // crea fecha en hora local
    return d.toLocaleDateString('es-CO', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    })
  }

  // Si viene con hora UTC, ajustar manualmente
  const d = new Date(val)
  if (isNaN(d.getTime())) return val

  const local = new Date(d.getTime() + d.getTimezoneOffset() * 60000)
  return local.toLocaleDateString('es-CO', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
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
}

.ext-filters__bottom {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}

.ext-filters__search {
  width: 100%;
  max-width: 650px;
}

.ext-filters__estado {
  width: 170px;
}

.ext-obs {
  display: inline-block;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ext-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}

.ext-chip--disponible {
  background: #e6f9f0;
  color: #1a8a55;
}

.ext-chip--creada {
  background: #e8f0fe;
  color: #1a56c4;
}

.ext-chip--eliminada {
  background: #fde8e8;
  color: #c0392b;
}

@media (max-width: 600px) {
  .ext-header {
    margin: 12px;
    padding: 20px;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
