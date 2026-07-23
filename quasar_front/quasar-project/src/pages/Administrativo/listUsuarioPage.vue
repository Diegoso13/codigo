<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Gestión de usuarios</div>

        <div class="asig-header__sub">{{ usuarios.length }} registros</div>
      </div>
    </div>

    <!-- ACCIONES -->
    <q-card class="shadow-card rounded-card q-mb-md">
      <q-card-section class="row items-center q-col-gutter-sm">
        <!-- Crear separado -->
        <div class="col-auto">
          <q-btn
            color="primary"
            icon="add"
            label="Nuevo"
            unelevated
            class="btn-action"
            @click="abrirDialogoCrear"
          />
        </div>

        <q-separator vertical class="q-mx-md" />

        <!-- Editar / eliminar -->
        <div class="col-auto">
          <q-btn
            color="warning"
            icon="edit"
            label="Actualizar"
            unelevated
            class="btn-action"
            :disable="!registroSeleccionado"
            @click="abrirDialogoEditar(registroSeleccionado)"
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
            @click="eliminarUsuario(registroSeleccionado.usuario)"
          />
        </div>

        <div class="col-grow" />

        <!-- FILTROS -->
        <div class="search-filters">
          <q-input
            v-model="filtros.search"
            outlined
            dense
            debounce="0"
            placeholder="Buscar..."
            class="search-filters__input"
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
        </div>
      </q-card-section>
    </q-card>

    <!-- TABLA -->
    <q-card class="shadow-card rounded-card">
      <q-card-section class="q-pa-none">
        <q-table
          :rows="usuarios"
          :columns="columns"
          row-key="usuario"
          flat
          bordered
          separator="horizontal"
          selection="single"
          v-model:selected="selected"
          :loading="loading"
          :pagination="{ rowsPerPage: 10 }"
          no-data-label="No hay usuarios."
          class="custom-table"
        >
          <template #loading>
            <q-inner-loading showing>
              <q-spinner-dots size="40px" color="primary" />
            </q-inner-loading>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- DIALOG CREAR/EDITAR USUARIO -->
    <q-dialog v-model="showDialog" persistent>
      <q-card style="min-width: 500px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">{{ esEditando ? 'Editar usuario' : 'Crear usuario' }}</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-form ref="formRef" @submit.prevent="guardarUsuario">
            <div class="row q-col-gutter-md q-mb-md">
              <div class="col-12">
                <q-input v-model="form.cliente" outlined dense label="Cliente *" :rules="[req]">
                  <template #prepend>
                    <q-icon name="business" />
                  </template>
                </q-input>
              </div>
              <div class="col-12">
                <q-input
                  v-model="form.usuario"
                  outlined
                  dense
                  label="Usuario *"
                  :rules="[req]"
                  :disable="esEditando"
                >
                  <template #prepend>
                    <q-icon name="person" />
                  </template>
                </q-input>
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.cedula" outlined dense label="Cédula *" :rules="[req]">
                  <template #prepend>
                    <q-icon name="badge" />
                  </template>
                </q-input>
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.cargo" outlined dense label="Cargo *" :rules="[req]">
                  <template #prepend>
                    <q-icon name="work" />
                  </template>
                </q-input>
              </div>
            </div>
          </q-form>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right">
          <q-btn flat label="Cancelar" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            color="primary"
            class="btn-action"
            :label="esEditando ? 'Actualizar' : 'Crear'"
            icon="save"
            type="submit"
            @click="guardarUsuario"
            :loading="loadingForm"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useUsuarios } from 'src/composables/useUsuarios'

const $q = useQuasar()

const { usuarios, loading, filtros, listar, eliminar, buscarConDebounce, crear, editar } =
  useUsuarios()

onMounted(() => {
  listar()
})

watch(
  () => filtros.value.search,
  () => buscarConDebounce(),
)

const selected = ref([])
const registroSeleccionado = computed(() => selected.value[0] || null)

// Estado del diálogo
const showDialog = ref(false)
const esEditando = ref(false)
const loadingForm = ref(false)
const formRef = ref(null)

const form = ref({
  cliente: '',
  usuario: '',
  cedula: '',
  cargo: '',
})

const req = (v) => !!v || 'Campo obligatorio'

function abrirDialogoCrear() {
  esEditando.value = false
  form.value = {
    cliente: '',
    usuario: '',
    cedula: '',
    cargo: '',
  }
  showDialog.value = true
}

function abrirDialogoEditar(registro) {
  esEditando.value = true
  form.value = { ...registro }
  showDialog.value = true
}

async function guardarUsuario() {
  const isValid = await formRef.value?.validate()
  if (!isValid) return

  loadingForm.value = true
  try {
    if (esEditando.value) {
      await editar(form.value.usuario, form.value)
    } else {
      await crear(form.value)
    }
    showDialog.value = false
    selected.value = []
  } catch {
    // Error manejado por el composable
  } finally {
    loadingForm.value = false
  }
}

function eliminarUsuario(id) {
  $q.dialog({
    title: 'Confirmar',
    message: `¿Deseas eliminar el usuario "${id}"?`,
    cancel: true,
    persistent: true,
  }).onOk(() => {
    void (async () => {
      eliminar(id)
    })()
  })
}

const columns = [
  { name: 'cliente', label: 'Cliente', field: 'cliente', align: 'left' },
  { name: 'usuario', label: 'Usuario', field: 'usuario', align: 'left' },
  { name: 'cedula', label: 'Cédula', field: 'cedula', align: 'left' },
  { name: 'cargo', label: 'Cargo', field: 'cargo', align: 'left' },
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

.search-filters {
  display: flex;
  gap: 10px;
}

.search-filters__input {
  width: 100%;
  max-width: 400px;
}

.custom-table {
  border-radius: 12px;
}
</style>
