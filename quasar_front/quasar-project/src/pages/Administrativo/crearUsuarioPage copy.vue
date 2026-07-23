<template>
  <q-page class="usu-page">
    <!-- HEADER -->
    <div class="usu-header">
      <q-btn flat round icon="arrow_back" color="white" @click="router.back()" />
      <div>
        <span class="usu-header__eyebrow">Usuarios</span>
        <h1 class="usu-header__title">{{ esEdicion ? 'Editar usuario' : 'Crear usuario' }}</h1>
        <p class="usu-header__sub">
          {{ esEdicion ? 'Actualiza los datos del usuario.' : 'Completa los datos para registrar un nuevo usuario.' }}
        </p>
      </div>
      
    </div>

    <div class="usu-body">
      <q-form  ref="formRef" class="usu-form" @submit.prevent="guardar">
        <div class="usu-card">
          <p class="usu-card__title">Datos del usuario</p>

          <div class="usu-grid">
            <q-input
              v-model="form.cliente"
              outlined dense
              label="Cliente *"
              :rules="[req]"
              class="usu-input"
            />
            <q-input
              v-model="form.usuario"
              outlined dense
              label="Usuario *"
              :rules="[req]"
              class="usu-input"
            />
            <q-input
              v-model="form.cedula"
              outlined dense
              label="Cédula *"
              :rules="[req]"
              class="usu-input"
            />
            <q-input
              v-model="form.cargo"
              outlined dense
              label="Cargo *"
              :rules="[req]"
              class="usu-input"
            />
          </div>
        </div>

         <!-- ACCIONES -->

        <div class="usu-actions">
          <q-btn flat label="Cancelar" class="usu-btn--cancel" @click="router.back()" />
          <q-btn unelevated color="primary" class="usu-btn" :label="esEdicion ? 'Actualizar' : 'Crear'" icon="save" type="submit"  />
        </div>
      </q-form>
    </div>

    
  </q-page>
</template>

<script setup>
import { ref, onMounted,computed  } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUsuarios } from 'src/composables/useUsuarios'

const {
  usuarios,
  listar,
  crear,
  editar,
} = useUsuarios()

const route = useRoute()
const router = useRouter()

const id = route.params.id // si existe → editar
const esEdicion = computed(() => !!id)

const form = ref({
  cliente: '',
  usuario: '',
  cedula: '',
  cargo: ''
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
    form.value = usuarios.value.find(u => u.usuario === usuario) || form.value
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
.usu-page {
  background: #f0f2f7;
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

.usu-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 28px 32px 24px;
  background: #1c2a45;
}

.usu-header__eyebrow {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #6fa3ef;
  margin-bottom: 4px;
}

.usu-header__title {
  margin: 0 0 2px;
  font-size: 22px;
  font-weight: 800;
  color: #fff;
}

.usu-header__sub {
  margin: 0;
  font-size: 13px;
  color: #7a8faf;
}

.usu-body {
  max-width: 680px;
  margin: 0 auto;
  padding: 28px 24px 48px;
}

.usu-card {
  background: #fff;
  border: 1px solid #e2e7f0;
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 16px;
}

.usu-card__title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #7a8faf;
  margin:  0 0 14px;
}

.usu-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.usu-input {
  width: 100%;
}

.usu-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.usu-btn {
  border-radius: 8px;
  font-weight: 600;
  padding: 0 24px;
  height: 40px;
}

.usu-btn--cancel {
  border-radius: 8px;
  font-weight: 600;
  color: #555;
}

.usu-error {
  background: #fff0f0;
  color: #c0392b;
  border-left: 3px solid #e74c3c;
}

@media (max-width: 600px) {
  .usu-header {
    padding: 20px 16px;
  }

  .usu-body {
    padding: 16px 12px 40px;
  }

  .usu-grid {
    grid-template-columns: 1fr;
  }
}
</style>