<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="lib-header">
      <div>
        <span class="lib-header__eyebrow">Extensiones</span>
        <h1 class="lib-header__title">Liberar extensión</h1>
        <p class="lib-header__sub">Selecciona una extensión para liberarla.</p>
      </div>
    </div>

    <!-- FILTROS ABAJO -->
    <div class="ext-filters__bottom">
      <q-input
        v-model="search"
        outlined
        dense
        debounce="400"
        placeholder="Buscar ticket, extensión, usuario..."
        class="ext-filters__search"
        @update:model-value="onSearch"
      >
        <template #prepend>
          <q-icon name="search" size="18px" />
        </template>
      </q-input>

      <q-select
        v-model="filtros.tipo_movimiento"
        :options="tipos"
        outlined
        dense
        clearable
        label="Tipo movimiento"
        class="ext-filters__estado"
        @update:model-value="listar"
      />
    </div>

    <div class="ext-table-wrap">
      <q-table
        :rows="movimientos"
        :columns="columns"
        row-key="id"
        flat
        :loading="loading"
        :pagination="{ rowsPerPage: 10 }"
        no-data-label="Sin movimientos."
        class="ext-table"
      >
        <template #body-cell-marca="props">
          <q-td :props="props">
            <q-badge color="primary">
              {{ props.row.marca }}
            </q-badge>
          </q-td>
        </template>

        <template #body-cell-tipo_movimiento="props">
          <q-td :props="props">
            <q-badge color="secondary">
              {{ props.row.tipo_movimiento }}
            </q-badge>
          </q-td>
        </template>

        <template #body-cell-fecha="props">
          <q-td :props="props">
            {{ formatDate(props.row.fecha) }}
          </q-td>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useMovimientos } from 'src/composables/useMovimientos'

const { movimientos, loading, filtros, listar } = useMovimientos()

/* SEARCH LOCAL */
const search = ref('')

/* PAGINATION (DRF compatible future-proof) */

/* OPTIONS */
const tipos = ['ASIGNACION', 'REASIGNACION', 'TRASLADO', 'LIBERACION']

/* COLUMNS */
const columns = [
  { name: 'ticket', label: 'Ticket', field: 'ticket', align: 'left' },
  { name: 'tipo_movimiento', label: 'Tipo', field: 'tipo_movimiento', align: 'left' },
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
  { name: 'fecha', label: 'Fecha', field: 'fecha', align: 'left' },
]

/* INIT */
onMounted(() => {
  listar()
})

/* SEARCH GLOBAL */
function onSearch(val) {
  filtros.value.search = val
  listar()
}

/* SERVER REQUEST (si quieres paginación real después) */

/* FORMAT DATE */
function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleString()
}
</script>

<style scoped>
.lib-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 32px 24px;
  background: #1c2a45;
}

.lib-header__back {
  flex-shrink: 0;
}

.lib-header__eyebrow {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #6fa3ef;
  margin-bottom: 4px;
}

.ext-filters {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 16px;
  margin-top: 20px;
}

.ext-filters__top {
  display: flex;
  justify-content: center;
}

.ext-filters__bottom {
  margin-top: 2%;
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

.lib-header__title {
  margin: 0 0 2px;
  font-size: 22px;
  font-weight: 800;
  color: #fff;
}

.lib-header__sub {
  margin: 0;
  font-size: 13px;
  color: #7a8faf;
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

.mov-page {
  padding: 20px;
  background: #f5f7fb;
}

.mov-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.mov-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

.mov-filters {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 12px;
}

.ext-table {
  margin-top: 2%;
  border-radius: 12px;
  border: 1px solid #e2e7f0;
  background: #fff;
}

.mov-filters {
  grid-template-columns: 1fr;
}

@media (max-width: 800px) {
  .ext-header {
    padding: 20px 16px;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .ext-filters {
    padding: 12px 16px;
  }

  .ext-table-wrap {
    flex: 1;
    padding: 20px 32px 32px;
  }
}
</style>
