<template>
  <div class="login-page flex" :style="backgroundStyle">
    <div class="absolute-top full-width q-pa-xl text-center">
      <h1 class="text-h2 text-weight-bolder text-white tracking-widest">LOLIC</h1>
    </div>

    <div class="login-sidebar flex flex-center">
      <q-card flat class="login-card bg-transparent">
        <q-card-section class="q-mb-md">
          <div class="text-h4 text-weight-bold">LOLIC</div>
          <div class="text-grey-7">Ingresa tus datos para iniciar sesión</div>
        </q-card-section>

        <q-form @submit="login">
          <q-card-section class="q-gutter-y-md">
            <q-input
              filled
              v-model="username"
              label="Usuario"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Este campo es obligatorio']"
            >
              <template v-slot:prepend><q-icon name="person" /></template>
            </q-input>

            <q-input
              filled
              v-model="password"
              type="password"
              label="Contraseña"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Este campo es obligatorio']"
            >
              <template v-slot:prepend><q-icon name="lock" /></template>
            </q-input>
          </q-card-section>

          <q-card-actions class="q-mt-lg">
            <q-btn
              type="submit"
              :style="{ backgroundColor: '#00105b', color: 'white' }"
              label="Iniciar Sesión"
              class="full-width text-weight-bold"
              size="lg"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </div>
  </div>
</template>

<script>
import { api } from 'boot/axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      // Imagen profesional para el fondo
      backgroundUrl:
        'https://www.semana.com/resizer/nvFheZq_NUldlYHkgnxKWFmU2VI=/arc-anglerfish-arc2-prod-semana/public/VBAR7UJ7QRAOBA4KGJO4I6N3GU.jpg',
    }
  },

  computed: {
    // Genera el estilo del fondo con un degradado para resaltar el texto blanco
    backgroundStyle() {
      return {
        backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(${this.backgroundUrl})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
      }
    },
  },

  methods: {
    async login() {
      try {
        // Petición POST al endpoint de login en Django
        const response = await api.post('auth/login/', {
          username: this.username,
          password: this.password,
        })


        console.log("RESPUESTA LOGIN:", response.data)

        // Almacenamiento local de la sesión (Token, Usuario y Rol)
        localStorage.setItem('token', response.data.access)
        localStorage.setItem('username', this.username)
        localStorage.setItem('rol', response.data.rol)

        // Redirección al Home tras éxito
        this.$router.push('/')
      } catch (error) {
        console.error(error)

        // Notificación de Quasar en caso de error
        this.$q.notify({
          type: 'negative',
          message: 'Credenciales incorrectas',
        })
      }
    },
  },
}
</script>

<style scoped>
.login-page {
  position: relative;
}

/* Columna lateral con efecto de desenfoque (glassmorphism) */
.login-sidebar {
  width: 450px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  height: 100%;
  box-shadow: 10px 0 25px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.login-card {
  width: 100%;
  max-width: 350px;
}

.tracking-widest {
  letter-spacing: 0.15em;
  text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
}

@media (max-width: 600px) {
  .login-sidebar {
    width: 100%;
  }
}
</style>
