<template>
  <q-page class="page-bg">
    <!-- HEADER -->
    <div class="asig-header">
      <div>
        <div class="asig-header__title">{{ esEdicion ? 'Editar usuario' : 'Crear usuario' }}</div>

        <div class="asig-header__sub">
          {{
            esEdicion
              ? 'Actualiza los datos del usuario.'
              : 'Completa los datos para registrar un nuevo usuario.'
          }}
        </div>
      </div>
    </div>

    <!-- FORM -->
    <q-card class="shadow-card rounded-card">
      <q-card-section>
        <div class="text-subtitle1 text-weight-bold q-mb-md">Datos del usuario</div>

        <q-form ref="formRef" @submit.prevent="guardar">
          <div class="row q-col-gutter-md q-mb-md">
            <div class="col-12 col-md-6">
              <q-input v-model="form.cliente" outlined dense label="Cliente *" :rules="[req]">
                <template #prepend>
                  <q-icon name="business" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-6">
              <q-input v-model="form.usuario" outlined dense label="Usuario *" :rules="[req]">
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

      <!-- ACTIONS -->
      <q-card-actions align="right" class="q-pa-md">
        <q-btn flat label="Cancelar" color="grey-7" @click="router.back()" />
        <q-btn
          unelevated
          color="primary"
          class="btn-action"
          :label="esEdicion ? 'Actualizar' : 'Crear'"
          icon="save"
          type="submit"
          @click="guardar"
        />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUsuarios } from 'src/composables/useUsuarios'

const { usuarios, listar, crear, editar } = useUsuarios()

const route = useRoute()
const router = useRouter()

const id = route.params.id // si existe → editar
const esEdicion = computed(() => !!id)

const form = ref({
  cliente: '',
  usuario: '',
  cedula: '',
  cargo: '',
})
const req = (v) => !!v || 'Campo obligatorio'
const loading = ref(false)

onMounted(() => {
  cargarUsuario()
})

const cargarUsuario = async () => {
  if (!id) return
  loading.value = true

  const usuario = id
  await listar({ usuario })
  form.value = usuarios.value.find((u) => u.usuario === usuario) || form.value
  loading.value = false
}

const guardar = async () => {
  loading.value = true

  if (id) {
    await editar(id, form.value)
  } else {
    await crear(form.value)
  }
  router.push('/usuarios')
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
