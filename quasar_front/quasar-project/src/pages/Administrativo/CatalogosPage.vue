<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Administración de Catálogos</div>

        <div class="asig-header__sub">
          Gestiona los catálogos de software, sedes, ciudades y propietarios
        </div>
      </div>
    </div>

    <!-- TABS -->
    <q-card class="shadow-card rounded-card q-mb-md">
      <q-card-section class="q-py-sm">
        <q-tabs v-model="tab" dense align="left" active-color="primary" indicator-color="primary">
          <q-tab name="software" label="Software" />
          <q-tab name="sedes" label="Sedes" />
          <q-tab name="ciudades" label="Ciudades" />
          <q-tab name="propietarios" label="Propietarios" />
        </q-tabs>
      </q-card-section>
    </q-card>

    <!-- ACCIONES -->
    <q-card class="q-mb-md shadow-card rounded-card">
      <q-card-section class="row items-center q-col-gutter-sm">
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

        <div class="col-auto">
          <q-btn
            color="warning"
            icon="edit"
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
            @click="confirmarEliminar(registroSeleccionado)"
          />
        </div>

        <div class="col-grow" />

        <div class="usu-filters">
          <q-input
            v-model="filtro"
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
                v-if="filtro"
                name="close"
                size="16px"
                class="cursor-pointer"
                @click="filtro = ''"
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
          :rows="rows"
          :columns="columns"
          row-key="id"
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
            {{ editando ? `Editar ${tituloActual}` : `Nuevo ${tituloActual}` }}
          </div>
          <q-btn dense flat round icon="close" v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-input v-model="nuevoNombre" :label="tituloActual" outlined dense autofocus>
            <template #prepend>
              <q-icon name="label" />
            </template>
          </q-input>
        </q-card-section>

        <q-card-actions align="right" class="q-pa-md">
          <q-btn flat label="Cancelar" color="grey-7" v-close-popup />
          <q-btn
            :label="editando ? 'Actualizar' : 'Guardar'"
            color="primary"
            unelevated
            @click="guardarDialog"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'

const $q = useQuasar()

const tab = ref('software')
const rows = ref([])
const dialog = ref(false)
const nuevoNombre = ref('')
const editando = ref(false)
const idEditando = ref(null)
const idEliminar = ref(null)
const selected = ref([])
const filtro = ref('')

const registroSeleccionado = computed(() => selected.value[0] || null)
const tituloActual = computed(() => {
  const map = {
    software: 'Software',
    sedes: 'Sede',
    ciudades: 'Ciudad',
    propietarios: 'Propietario',
  }

  return map[tab.value] || 'registro'
})

const columns = [
  {
    name: 'id',
    label: 'ID',
    field: 'id',
    align: 'left',
  },
  {
    name: 'nombre',
    label: 'Nombre',
    field: 'nombre',
    align: 'left',
  },
]

function abrirDialogCrear() {
  editando.value = false
  idEditando.value = null
  nuevoNombre.value = ''
  dialog.value = true
}

function abrirDialogEditar() {
  if (!registroSeleccionado.value) return
  editarRegistro(registroSeleccionado.value)
}

function editarRegistro(row) {
  editando.value = true
  idEditando.value = row.id
  nuevoNombre.value = row.nombre
  dialog.value = true
}
function confirmarEliminar(row) {
  idEliminar.value = row.id
  $q.dialog({
    title: 'Confirmar',
    message: `¿Eliminar "${row.nombre}"?`,
    cancel: true,
    persistent: true,
  }).onOk(() => {
    eliminarRegistro()
  })
}

async function cargarDatos() {
  try {
    const response = await api.get(`catalogos/${tab.value}/`)
    rows.value = response.data
  } catch (error) {
    console.error(error)
  }
}

async function guardar() {
  try {
    if (editando.value) {
      await api.put(`catalogos/${tab.value}/${idEditando.value}/`, {
        nombre: nuevoNombre.value,
      })
    } else {
      await api.post(`catalogos/${tab.value}/`, {
        nombre: nuevoNombre.value,
      })
    }
    dialog.value = false
    selected.value = []
    cargarDatos()
  } catch (error) {
    console.error(error)
  }
}

async function guardarDialog() {
  await guardar()
}

async function eliminarRegistro() {
  try {
    await api.delete(`catalogos/${tab.value}/${idEliminar.value}/`)
    selected.value = []
    cargarDatos()
    $q.notify({
      type: 'positive',
      message: 'Registro eliminado',
    })
  } catch (error) {
    console.error(error)
    $q.notify({
      type: 'negative',
      message: 'Error al eliminar',
    })
  }
}

watch(tab, () => {
  selected.value = []
  filtro.value = ''
  cargarDatos()
})
onMounted(() => {
  cargarDatos()
})
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

.usu-filters {
  min-width: 260px;
}

.usu-filters__search {
  width: 100%;
}

.custom-table :deep(.q-table__top) {
  padding: 12px;
}

.custom-table :deep(.q-table thead tr th) {
  background: #fafafa;
  font-weight: 700;
  color: #374151;
}

@media (max-width: 700px) {
  .page-bg {
    padding: 18px;
  }

  .asig-header {
    padding: 22px;
  }

  .usu-filters {
    width: 100%;
    min-width: 0;
  }
}
</style>
