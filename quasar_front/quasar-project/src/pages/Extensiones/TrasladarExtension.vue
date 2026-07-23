<template>
  <q-page class="asig-page">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">Intercambiar extensión</div>

        <div class="asig-header__sub">Los usuarios intercambiaran extensiones.</div>
      </div>
    </div>

    <!-- BODY -->
    <div class="asig-body">
      <!-- Extension1 -->
      <div class="asig-card">
        <p class="asig-card__title">Extensión 1</p>

        <q-select
          v-model="extension1"
          outlined
          dense
          use-input
          input-debounce="300"
          clearable
          label="Buscar extensión referencia"
          class="asig-input"
          :options="options1"
          @filter="filtrarExtension1"
          emit-value
          map-options
          @update:model-value="cargarExt1"
        >
          <template #prepend>
            <q-icon name="dialpad" />
          </template>
        </q-select>

        <div v-if="ext1" class="q-mt-md">
          <q-table
            :rows="[ext1]"
            :columns="columnasReferencia"
            row-key="extension"
            flat
            bordered
            dense
            hide-pagination
            :rows-per-page-options="[0]"
            class="asig-table"
          >
            <template #body-cell-estado="props">
              <q-td :props="props">
                <span :class="chipClass(props.row.estado)">
                  {{ props.row.estado }}
                </span>
              </q-td>
            </template>

            <template #body-cell-observacion="props">
              <q-td :props="props">
                {{ props.row.observacion || '—' }}
              </q-td>
            </template>
          </q-table>
        </div>
      </div>

      <!-- Extension2 -->
      <div class="asig-card">
        <p class="asig-card__title">Extensión 2</p>

        <q-select
          v-model="extension2"
          outlined
          dense
          use-input
          input-debounce="300"
          clearable
          label="Buscar extensión referencia"
          class="asig-input"
          :options="options2"
          @filter="filtrarExtension2"
          emit-value
          map-options
          @update:model-value="cargarExt2"
        >
          <template #prepend>
            <q-icon name="dialpad" />
          </template>
        </q-select>

        <div v-if="ext2" class="q-mt-md">
          <q-table
            :rows="[ext2]"
            :columns="columnasReferencia"
            row-key="extension"
            flat
            bordered
            dense
            hide-pagination
            :rows-per-page-options="[0]"
            class="asig-table"
          >
            <template #body-cell-estado="props">
              <q-td :props="props">
                <span :class="chipClass(props.row.estado)">
                  {{ props.row.estado }}
                </span>
              </q-td>
            </template>

            <template #body-cell-observacion="props">
              <q-td :props="props">
                {{ props.row.observacion || '—' }}
              </q-td>
            </template>
          </q-table>
        </div>
      </div>

      <!-- BOTON -->
      <div class="inter-actions q-mt-md">
        <q-btn
          color="primary"
          label="Intercambiar"
          :disable="!canProceed"
          @click="showForm = true"
        />
      </div>

      <!-- FORMULARIO -->
      <div v-if="showForm" class="q-mt-lg">
        <div class="inter-grid inter-grid--2">
          <!-- EXT 1 FORM -->
          <div class="inter-card">
            <p class="inter-card__title">Extensión 1</p>

            <q-input v-model="form1.extension" label="Extensión" outlined dense disable />

            <q-input v-model="form2.usuario" label="Usuario" outlined dense disable />

            <q-select
              v-model="form2.direccion"
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
              v-model="form2.campana"
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
              v-model="form2.sede"
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
              v-model="form2.cliente2"
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
              v-model="form2.ceco"
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

            <q-select
              v-model="form2.codigoceco"
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

            <q-input v-model="form2.observacion" label="Observación" outlined dense />
          </div>

          <!-- EXT 2 FORM -->
          <div class="inter-card">
            <p class="inter-card__title">Extensión 2</p>

            <q-input v-model="form2.extension" label="Extensión" outlined dense disable />

            <q-input v-model="form1.usuario" label="Usuario" outlined dense disable />

            <q-select
              v-model="form1.direccion"
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
              v-model="form1.campana"
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
              v-model="form1.sede"
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
              v-model="form1.cliente2"
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
              v-model="form1.ceco"
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

            <q-select
              v-model="form1.codigoceco"
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

            <q-input v-model="form1.observacion" label="Observación" outlined dense />
          </div>
        </div>

        <!-- TICKET -->
        <div class="inter-card q-mt-md">
          <q-input v-model="ticket" label="Ticket solicitud" outlined dense />
        </div>

        <!-- ENVIAR -->
        <div class="inter-actions q-mt-md">
          <q-btn color="primary" label="Confirmar intercambio" :loading="loading" @click="enviar" />
        </div>
      </div>
    </div>
    <q-dialog v-model="showMovDialog">
      <q-card style="min-width: 1200px">
        <q-card-section class="text-h6"> Movimientos generados </q-card-section>

        <q-separator />

        <q-card-section>
          <q-table
            :rows="movimientos"
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

import { useExtensiones } from 'src/composables/useExtensiones'
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

const { extensiones, loading, listar, trasladarModificar } = useExtensiones()

const direccionCrud = useDireccion()
const campanaCrud = useCampana()
const sedeCrud = useSede()
const cliente2Crud = useCliente2()
const cecoCrud = useCeco()
const codigoCecoCrud = useCodigoCeco()

///// EXTENSIONES

const extension1 = ref(null)
const extension2 = ref(null)

const options1 = ref([])
const options2 = ref([])

const ext1 = ref(null)
const ext2 = ref(null)

////////   FORM

const showForm = ref(false)

const form1 = ref({})
const form2 = ref({})

const ticket = ref('')

/* =====================
   VALIDACION
===================== */
const canProceed = computed(
  () => extension1.value && extension2.value && extension1.value !== extension2.value,
)

/* =====================
   EXTENSIONES LISTAR
===================== */

async function filtrarExtension1(val, update) {
  await listar({ search: val || '', estado: 'CREADA' })

  update(() => {
    options1.value = extensiones.value.map((e) => ({
      label: e.extension,
      value: e.extension,
    }))
  })
}

async function filtrarExtension2(val, update) {
  await listar({ search: val || '', estado: 'CREADA' })

  update(() => {
    options2.value = extensiones.value.map((e) => ({
      label: e.extension,
      value: e.extension,
    }))
  })
}

///CARGAR EXTENSIONES

async function cargarExt1(val) {
  ext1.value = extensiones.value.find((e) => e.extension === val) || null
  form1.value = { ...ext1.value }
}

async function cargarExt2(val) {
  ext2.value = extensiones.value.find((e) => e.extension === val) || null
  form2.value = { ...ext2.value }
}

//// COLUMNAS TABLA

const columnasReferencia = [
  { name: 'extension', label: 'Extensión', field: 'extension', align: 'left' },
  { name: 'cliente', label: 'Cliente', field: 'cliente', align: 'left' },
  { name: 'direccion', label: 'Dirección', field: 'direccion', align: 'left' },
  { name: 'tipo', label: 'Tipo', field: 'tipo', align: 'left' },
  { name: 'division', label: 'División', field: 'division', align: 'left' },
  { name: 'campana', label: 'Campaña', field: 'campana', align: 'left' },
  { name: 'plataforma', label: 'Plataforma', field: 'plataforma', align: 'left' },
  { name: 'codigo_ceco', label: 'Código CECO', field: 'codigo_ceco', align: 'left' },
  { name: 'ceco', label: 'CECO', field: 'ceco', align: 'left' },
  { name: 'cliente2', label: 'Cliente 2', field: 'cliente2', align: 'left' },
  { name: 'cedula', label: 'Cédula', field: 'cedula', align: 'left' },
  { name: 'usuario', label: 'Usuario', field: 'usuario', align: 'left' },
  { name: 'puesto_trabajo', label: 'Puesto trabajo', field: 'puesto_trabajo', align: 'left' },
  { name: 'sede', label: 'Sede', field: 'sede', align: 'left' },
  { name: 'cargo', label: 'Cargo', field: 'cargo', align: 'left' },
  { name: 'ticket_solicitud', label: 'Ticket solicitud', field: 'ticket_solicitud', align: 'left' },
  {
    name: 'ticket_eliminacion',
    label: 'Ticket eliminación',
    field: 'ticket_eliminacion',
    align: 'left',
  },
  { name: 'estado', label: 'Estado', field: 'estado', align: 'left' },
  { name: 'observacion', label: 'Observación', field: 'observacion', align: 'left' },
]

//SELECT FILTRADOS

const direccionesFiltradas = ref([])
const campanasFiltradas = ref([])
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

////// ENVIAR

async function enviar() {
  const res = await trasladarModificar({
    extension1: ext1.value.extension,
    extension2: ext2.value.extension,
    datos_extension1: form1.value,
    datos_extension2: form2.value,
    ticket: ticket.value,
  })

  movimientos.value = res?.movimientos || []
  showMovDialog.value = true
}

///CHIP ESTADO

function chipClass(estado) {
  const base = 'asig-chip'
  const map = {
    DISPONIBLE: 'asig-chip--disponible',
    CREADA: 'asig-chip--creada',
    ELIMINADA: 'asig-chip--eliminada',
  }
  return `${base} ${map[estado] ?? ''}`
}

///mostrar movimiento

function cerrarDialog() {
  showMovDialog.value = false
  router.push('/extensiones')
}

const showMovDialog = ref(false)
const movimientos = ref([])

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
.asig-page {
  background: #f0f2f7;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

.asig-body {
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 24px 48px;
}

/* =========================
   HEADER
========================= */
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

/* =========================
   CARDS
========================= */
.asig-card,
.inter-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 18px;
  border: 1px solid #e6e8ef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.asig-card:hover,
.inter-card:hover {
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
}

.asig-card__title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #7a8faf;
  margin: 0 0 14px;
}

/* =========================
   GRID
========================= */
.asig-grid,
.inter-grid {
  display: grid;
  gap: 16px;
}

.asig-grid--2,
.inter-grid--2 {
  grid-template-columns: repeat(2, 1fr);
}

@media (max-width: 900px) {
  .asig-grid--2,
  .inter-grid--2 {
    grid-template-columns: 1fr;
  }
}

/* =========================
   INPUTS
========================= */
.asig-input,
.q-input,
.q-select {
  width: 100%;
}

.q-field__control {
  border-radius: 10px !important;
}

.q-field--outlined .q-field__control {
  background: #fafbff;
}

/* spacing dentro de cards */
.inter-card .q-input,
.inter-card .q-select {
  margin-bottom: 12px;
}

/* =========================
   BUTTON ACTIONS
========================= */
.asig-actions,
.inter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.inter-actions .q-btn {
  border-radius: 10px;
  padding: 8px 18px;
  font-weight: 600;
  text-transform: none;
  transition: all 0.2s ease;
}

/* botón primario con hover */
.inter-actions .q-btn.bg-primary {
  background: linear-gradient(135deg, #1976d2, #1565c0) !important;
}

.inter-actions .q-btn:hover {
  transform: translateY(-1px);
}

/* disabled */
.inter-actions .q-btn[disabled] {
  opacity: 0.5;
  box-shadow: none;
}

/* =========================
   CHIP ESTADO
========================= */
.asig-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.asig-chip--creada {
  background: #e8f0fe;
  color: #1a56c4;
}

.inter-card__title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #7a8faf;
  margin: 0 0 12px;
}
</style>
