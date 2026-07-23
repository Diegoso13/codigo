<template>
  <q-page class="reasig-page">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Reasignar extensión</div>

        <div class="asig-header__sub">
          El usuario quedara en una extension que se encuentra en estado CREADA.
        </div>
      </div>
    </div>

    <!-- BODY -->
    <div class="reasig-body">
      <!-- EXTENSIÓN REFERENCIA -->
      <div class="reasig-card">
        <p class="reasig-card__title">Extensión a reasignar</p>

        <q-select
          v-model="extensionReferencia"
          outlined
          dense
          use-input
          input-debounce="300"
          clearable
          label="Buscar extensión"
          class="reasig-input"
          :options="extensionesRefFiltradas"
          @filter="filtrarExtensionesRef"
          emit-value
          map-options
          @update:model-value="cargarExtensionReferencia"
        >
          <template #prepend>
            <q-icon name="dialpad" />
          </template>
        </q-select>

        <div v-if="extensionRefObj" class="q-mt-sm text-grey-7">
          <b>Estado:</b> {{ extensionRefObj.estado }} | <b>Tipo:</b> {{ extensionRefObj.tipo }} |
          <b>División:</b> {{ extensionRefObj.division }} | <b>Plataforma:</b>
          {{ extensionRefObj.plataforma }}
        </div>

        <q-banner
          v-if="extensionReferencia && !extensionRefObj"
          dense
          rounded
          class="reasig-error q-mt-md"
          icon="warning"
        >
          No se encontró información para esta extensión.
        </q-banner>
      </div>

      <!-- FORMULARIO -->
      <q-form ref="formRef" class="reasig-form" @submit.prevent="enviar">
        <!-- EXTENSION SELECCIONADA -->
        <div class="reasig-card">
          <p class="reasig-card__title">
            Extensión seleccionada <span class="reasig-required">*</span>
          </p>

          <q-input
            v-model="form.extension"
            outlined
            dense
            label="Extensión"
            class="reasig-input"
            disable
            :rules="[(val) => !!val || 'La extensión es obligatoria']"
          >
            <template #prepend>
              <q-icon name="dialpad" />
            </template>
          </q-input>
        </div>

        <!-- NUEVO USUARIO -->
        <div class="reasig-card">
          <p class="reasig-card__title">Nuevo usuario</p>

          <div class="reasig-grid">
            <q-select
              v-model="form.usuario"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Usuario"
              class="reasig-input"
              :options="usuariosFiltrados"
              @filter="filtrarUsuarios"
              :disable="loading"
              :rules="[(val) => !!val || 'El usuario es obligatorio']"
            >
            </q-select>

            <q-input
              v-model="form.puesto_trabajo"
              outlined
              dense
              label="Puesto de trabajo"
              class="reasig-input"
              :disable="loading"
            >
            </q-input>
          </div>
        </div>

        <!-- ORGANIZACION -->
        <div class="reasig-card">
          <p class="reasig-card__title">Organización</p>

          <div class="reasig-grid">
            <q-select
              v-model="form.direccion"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Dirección"
              class="reasig-input"
              :options="direccionesFiltradas"
              @filter="filtrarDirecciones"
              :disable="loading"
            >
            </q-select>

            <q-select
              v-model="form.campana"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Campaña"
              class="reasig-input"
              :options="campanasFiltradas"
              @filter="filtrarCampanas"
              :disable="loading"
            >
            </q-select>

            <q-select
              v-model="form.sede"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Sede"
              class="reasig-input"
              :options="sedesFiltradas"
              @filter="filtrarSedes"
              :disable="loading"
            >
            </q-select>

            <q-select
              v-model="form.cliente2"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Cliente 2"
              class="reasig-input"
              :options="clientes2Filtrados"
              @filter="filtrarClientes2"
              :disable="loading"
            >
            </q-select>

            <q-select
              v-model="form.codigoceco"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="Código CECO"
              class="reasig-input"
              :options="codigoCecoFiltrados"
              @filter="filtrarCodigoCeco"
              :disable="loading"
            >
            </q-select>

            <q-select
              v-model="form.ceco"
              outlined
              dense
              use-input
              input-debounce="300"
              clearable
              label="CECO"
              class="reasig-input"
              :options="cecoFiltrados"
              @filter="filtrarCeco"
              :disable="loading"
            >
            </q-select>
          </div>
        </div>

        <!-- TRAZABILIDAD -->
        <div class="reasig-card">
          <p class="reasig-card__title">Trazabilidad</p>

          <div class="reasig-grid reasig-grid--full">
            <q-input
              v-model="form.ticket_solicitud"
              outlined
              dense
              label="Ticket de solicitud *"
              class="reasig-input"
              :disable="loading"
              :rules="[(val) => !!val || 'El ticket es obligatorio']"
            >
            </q-input>

            <q-input
              v-model="form.observacion"
              outlined
              dense
              label="Observación"
              type="textarea"
              autogrow
              class="reasig-input"
              :disable="loading"
            >
            </q-input>
          </div>
        </div>

        <!-- ACCIONES -->
        <div class="reasig-actions">
          <q-btn flat label="Cancelar" class="reasig-btn--cancel" @click="router.back()" />

          <q-btn
            unelevated
            type="submit"
            label="Reasignar extensión"
            color="primary"
            class="reasig-btn"
            :loading="loading"
            :disable="!form.extension"
          />
        </div>
      </q-form>
    </div>

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
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useExtensiones } from 'src/composables/useExtensiones'
import { useUsuarios } from 'src/composables/useUsuarios'
import {
  useDireccion,
  useCampana,
  useSede,
  useCliente2,
  useCeco,
  useCodigoCeco,
} from 'src/composables/useCatalogo'

const router = useRouter()

////// COMPOSABLES

const { extensiones, loading, listar, reasignar } = useExtensiones()
const { usuarios, listar: listarUsuarios } = useUsuarios()

const direccionCrud = useDireccion()
const campanaCrud = useCampana()
const sedeCrud = useSede()
const cliente2Crud = useCliente2()
const cecoCrud = useCeco()
const codigoCecoCrud = useCodigoCeco()

/* ==========================
   FORM
========================== */
const formRef = ref(null)

const form = reactive({
  extension: '',
  usuario: '',
  puesto_trabajo: '',
  direccion: '',
  campana: '',
  sede: '',
  cliente2: '',
  codigoceco: '',
  ceco: '',
  ticket_solicitud: '',
  observacion: '',
})

/* ==========================
   EXTENSION REFERENCIA
========================== */
const extensionReferencia = ref(null)
const extensionRefObj = ref(null)

const extensionesRefFiltradas = ref([])

async function filtrarExtensionesRef(val, update) {
  update(() => {
    extensionesRefFiltradas.value = []
  })
  await listar({ search: val || '', estado: 'CREADA' })

  update(() => {
    extensionesRefFiltradas.value = extensiones.value.map((e) => ({
      label: e.extension,
      value: e.extension,
    }))
  })
}

async function cargarExtensionReferencia(ext) {
  if (!ext) {
    extensionRefObj.value = null

    Object.assign(form, {
      extension: '',
      usuario: '',
      puesto_trabajo: '',
      direccion: '',
      campana: '',
      sede: '',
      cliente2: '',
      codigoceco: '',
      ceco: '',
      ticket_solicitud: '',
      observacion: '',
    })

    return
  }

  await listar({ extension: ext })
  extensionRefObj.value = extensiones.value?.[0] ?? null

  if (!extensionRefObj.value) return

  Object.assign(form, {
    extension: extensionRefObj.value.extension || '',
    usuario: '', // IMPORTANTE: debe ser nuevo usuario
    puesto_trabajo: extensionRefObj.value.puesto_trabajo || '',
    direccion: extensionRefObj.value.direccion || '',
    campana: extensionRefObj.value.campana || '',
    sede: extensionRefObj.value.sede || '',
    cliente2: extensionRefObj.value.cliente2 || '',
    codigoceco: extensionRefObj.value.codigoceco || '',
    ceco: extensionRefObj.value.ceco || '',
    ticket_solicitud: '',
    observacion: '',
  })
}

//SELECT FILTRADOS

const direccionesFiltradas = ref([])
const campanasFiltradas = ref([])
const usuariosFiltrados = ref([])
const sedesFiltradas = ref([])
const clientes2Filtrados = ref([])
const codigoCecoFiltrados = ref([])
const cecoFiltrados = ref([])

async function filtrarDirecciones(val, update) {
  update(() => {
    direccionesFiltradas.value = []
  })

  await direccionCrud.listar({ search: val || '' })
  direccionesFiltradas.value = direccionCrud.items.value.map((x) => x.direccion)
}

async function filtrarCampanas(val, update) {
  update(() => {
    campanasFiltradas.value = []
  })

  await campanaCrud.listar({ search: val || '' })
  campanasFiltradas.value = campanaCrud.items.value.map((x) => x.campana)
}

async function filtrarUsuarios(val, update) {
  update(() => {
    usuariosFiltrados.value = []
  })

  await listarUsuarios({ search: val || '' })
  usuariosFiltrados.value = usuarios.value.map((u) => u.usuario)
}

async function filtrarSedes(val, update) {
  update(() => {
    sedesFiltradas.value = []
  })

  await sedeCrud.listar({ search: val || '' })
  sedesFiltradas.value = sedeCrud.items.value.map((x) => x.sede)
}

async function filtrarClientes2(val, update) {
  update(() => {
    clientes2Filtrados.value = []
  })

  await cliente2Crud.listar({ search: val || '' })
  clientes2Filtrados.value = cliente2Crud.items.value.map((x) => x.cliente2)
}

async function filtrarCodigoCeco(val, update) {
  update(() => {
    codigoCecoFiltrados.value = []
  })

  await codigoCecoCrud.listar({ search: val || '' })
  codigoCecoFiltrados.value = codigoCecoCrud.items.value.map((x) => x.codigoceco)
}

async function filtrarCeco(val, update) {
  update(() => {
    cecoFiltrados.value = []
  })

  await cecoCrud.listar({ search: val || '' })
  cecoFiltrados.value = cecoCrud.items.value.map((x) => x.ceco)
}

/* ==========================
   ENVIAR
========================== */

async function enviar() {
  const valido = await formRef.value?.validate()
  if (valido !== true) return

  if (!form.extension) return

  const res = await reasignar({ ...form })

  movimientoActual.value = res?.movimientos?.[0] || res?.movimiento || null

  showMovDialog.value = true
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
.reasig-page {
  background: #f0f2f7;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

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

.reasig-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 24px 48px;
}

.reasig-card {
  background: #fff;
  border: 1px solid #e2e7f0;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 16px;
}

.reasig-card__title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #7a8faf;
  margin: 0 0 14px;
}

.reasig-required {
  color: #e74c3c;
}

.reasig-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.reasig-grid--full {
  grid-template-columns: 1fr;
}

.reasig-input {
  width: 100%;
}

.reasig-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.reasig-btn {
  border-radius: 8px;
  font-weight: 600;
  padding: 0 24px;
  height: 40px;
}

.reasig-btn--cancel {
  border-radius: 8px;
  font-weight: 600;
  color: #555;
}

.reasig-error {
  background: #fff0f0;
  color: #c0392b;
  border-left: 3px solid #e74c3c;
}

@media (max-width: 600px) {
  .reasig-header {
    padding: 20px 16px;
  }

  .reasig-body {
    padding: 16px 12px 40px;
  }

  .reasig-grid {
    grid-template-columns: 1fr;
  }
}
</style>
