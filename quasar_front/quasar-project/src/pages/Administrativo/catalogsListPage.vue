<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Catálogos</div>

        <div class="asig-header__sub">
          Administra direcciones, campañas, sedes y cliente 2 del sistema
        </div>
      </div>
    </div>

    <q-card class="q-mb-md shadow-card rounded-card">
      <q-separator />

      <q-card-section class="q-py-sm">
        <q-tabs v-model="tab" dense align="left" active-color="primary" indicator-color="primary">
          <q-tab name="direccion" label="Direcciones" />
          <q-tab name="campana" label="Campañas" />
          <q-tab name="sede" label="Sedes" />
          <q-tab name="cliente2" label="Cliente 2" />
          <q-tab name="ceco" label="CECO" />
          <q-tab name="codigoceco" label="Código CECO" />
        </q-tabs>
      </q-card-section>
    </q-card>

    <!-- ACCIONES -->
    <q-card class="q-mb-md shadow-card rounded-card">
      <q-card-section class="row items-center q-col-gutter-sm">
        <!-- Crear separado -->
        <div class="col-auto">
          <q-btn
            color="primary"
            icon="add"
            label="Nuevo"
            unelevated
            class="btn-action"
            @click="abrirDialogCrear"
          />
        </div>

        <q-separator vertical class="q-mx-md" />

        <!-- Editar / eliminar -->
        <div class="col-auto">
          <q-btn
            color="warning"
            icon="edit"
            row-key="usuario"
            label="Actualizar"
            unelevated
            class="btn-action"
            :disable="!registroSeleccionado"
            @click="abrirDialogEditar"
          />
        </div>

        <div class="col-auto">
          <q-btn
            color="negative"
            icon="delete"
            label="Eliminar"
            unelevated
            class="btn-action"
            :disable="!registroSeleccionado"
            @click="eliminarRegistro"
          />
        </div>

        <div class="col-grow" />

        <!-- FILTROS -->
        <div class="usu-filters">
          <q-input
            v-model="config.crud.filtros.value.search"
            outlined
            dense
            debounce="0"
            placeholder="Buscar..."
            class="usu-filters__search"
          >
            <template #prepend>
              <q-icon name="search" size="18px" />
            </template>

            <template #append>
              <q-icon
                v-if="config.crud.filtros.value.search"
                name="close"
                size="16px"
                class="cursor-pointer"
                @click="config.crud.filtros.value.search = ''"
              />
            </template>
          </q-input>
        </div>
      </q-card-section>
    </q-card>

    <!-- TABLA -->
    <q-card class="shadow-card rounded-card">
      <q-card-section class="q-pa-none">
        <q-table
          :rows="rowsActuales"
          :columns="columns"
          row-key="valor"
          :loading="loadingActual"
          :filter="filtro"
          selection="single"
          v-model:selected="selected"
          flat
          bordered
          separator="horizontal"
          class="custom-table"
        >
          <template v-slot:no-data>
            <div class="text-grey-7 q-pa-md text-center">No hay registros.</div>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- DIALOG -->
    <q-dialog v-model="dialog" persistent>
      <q-card style="min-width: 460px" class="rounded-card">
        <q-card-section class="row items-center justify-between">
          <div class="text-subtitle1 text-weight-bold">
            {{ modoEdicion ? `Editar ${tituloActual}` : `Nueva ${tituloActual}` }}
          </div>

          <q-btn dense flat round icon="close" v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-input v-model="form.valor" outlined dense :label="tituloActual" autofocus>
            <template v-slot:prepend>
              <q-icon name="location_on" />
            </template>
          </q-input>
        </q-card-section>

        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat label="Cancelar" color="grey-7" v-close-popup />
          <q-btn
            color="primary"
            unelevated
            :label="modoEdicion ? 'Actualizar' : 'Guardar'"
            @click="guardarRegistro"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import {
  useDireccion,
  useCodigoCeco,
  useCeco,
  useSede,
  useCampana,
  useCliente2,
} from 'src/composables/useCatalogo'

const $q = useQuasar()

const tab = ref('direccion')

const direccionCrud = useDireccion()
const codigoCecoCrud = useCodigoCeco()
const cecoCrud = useCeco()
const sedeCrud = useSede()
const campanaCrud = useCampana()
const cliente2Crud = useCliente2()

const selected = ref([])
const registroSeleccionado = computed(() => selected.value[0] || null)

const dialog = ref(false)
const modoEdicion = ref(false)

const form = ref({
  valor: '',
})

const config = computed(() => {
  const map = {
    direccion: {
      titulo: 'Dirección',
      crud: direccionCrud,
      field: 'direccion',
    },

    codigoceco: {
      titulo: 'Código CECO',
      crud: codigoCecoCrud,
      field: 'codigoceco',
    },

    ceco: {
      titulo: 'CECO',
      crud: cecoCrud,
      field: 'ceco',
    },
    sede: {
      titulo: 'Sede',
      crud: sedeCrud,
      field: 'sede',
    },
    campana: {
      titulo: 'Campaña',
      crud: campanaCrud,
      field: 'campana',
    },
    cliente2: {
      titulo: 'Cliente 2',
      crud: cliente2Crud,
      field: 'cliente2',
    },
  }

  return map[tab.value]
})

const tituloActual = computed(() => config.value.titulo)
const loadingActual = computed(() => config.value.crud.loading.value)

const rowsActuales = computed(() => {
  return config.value.crud.items.value.map((x) => ({
    valor: x[config.value.field],
  }))
})

async function listarActual() {
  await config.value.crud.listar()
}

onMounted(async () => {
  await listarActual()
})

watch(tab, async () => {
  selected.value = []
  await listarActual()
})

watch(
  () => config.value.crud.filtros.value.search,
  () => config.value.crud.buscarConDebounce(),
)

function abrirDialogCrear() {
  modoEdicion.value = false
  form.value.valor = ''
  dialog.value = true
}

function abrirDialogEditar() {
  if (!registroSeleccionado.value) return
  modoEdicion.value = true
  form.value.valor = registroSeleccionado.value.valor
  dialog.value = true
}

async function guardarRegistro() {
  const valor = form.value.valor.trim()
  if (!valor) return

  const field = config.value.field

  if (modoEdicion.value && registroSeleccionado.value) {
    const anterior = registroSeleccionado.value.valor
    await config.value.crud.editar(anterior, { [field]: valor })
  } else {
    await config.value.crud.crear({ [field]: valor })
  }

  dialog.value = false
  selected.value = []
  await listarActual()
}

function eliminarRegistro() {
  if (!registroSeleccionado.value) return

  $q.dialog({
    title: 'Confirmar',
    message: `¿Deseas eliminar "${registroSeleccionado.value.valor}"?`,
    cancel: true,
    persistent: true,
  }).onOk(async () => {
    await config.value.crud.eliminar(registroSeleccionado.value.valor)
    selected.value = []
    await listarActual()
  })
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

<style scoped>
.reasig-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 32px 24px;
  background: #1c2a45;
}

.reasig-header__back {
  flex-shrink: 0;
}

.reasig-header__eyebrow {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #6fa3ef;
  margin-bottom: 4px;
}

.reasig-header__title {
  margin: 0 0 2px;
  font-size: 22px;
  font-weight: 800;
  color: #fff;
}

.reasig-header__sub {
  margin: 0;
  font-size: 13px;
  color: #7a8faf;
}
.page-bg {
  background: #f0f2f7;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
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
  font-weight: 600;
}

.search-input {
  border-radius: 12px;
}

.total-box {
  margin-left: auto;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 8px 14px;
  min-width: 90px;
  text-align: center;
}

.total-label {
  font-size: 12px;
  color: #6b7280;
  line-height: 14px;
}

.total-value {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.custom-table :deep(.q-table__top) {
  padding: 12px;
}

.custom-table :deep(.q-table thead tr th) {
  background: #fafafa;
  font-weight: 700;
  color: #374151;
}
</style>
