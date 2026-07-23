import { ref } from 'vue'
import {usuarioService} from  'src/services/usuarioService'
import { notifyError, notifySuccess } from 'src/utils/notify'

export function useUsuarios() {

  const usuarios = ref([])
  const loading = ref(false)


  const filtros = ref({
    search: ''
  })

  let timeout = null

  const listar = async (params) => {
    loading.value = true

    try {
      const { data } = await usuarioService.listar({search: filtros.value.search || null, ...params})

      usuarios.value = Array.isArray(data) ? data : data.results ?? []

    } catch (e) {
      notifyError(e)
    } finally {
      loading.value = false
    }
  }
  const buscarConDebounce = () => {
    clearTimeout(timeout)

    timeout = setTimeout(() => {
      listar()
    }, 400)
  }

  const crear = async (payload) => {
    loading.value = true

    try {
      const { data } = await usuarioService.crear(payload)

      usuarios.value = [data, ...usuarios.value]

      notifySuccess('Usuario creado correctamente')
      return data

    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  const editar = async (usuario, payload) => {
    loading.value = true

    try {
      const { data } = await usuarioService.editar(usuario, payload)

      const idx = usuarios.value.findIndex(u => u.id === usuario)
      if (idx !== -1) usuarios.value[idx] = data

      notifySuccess('Usuario actualizado correctamente')
      return data

    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  const eliminar = async (usuario) => {
    loading.value = true

    try {
      await usuarioService.eliminar(usuario)

      usuarios.value = usuarios.value.filter(u => u.id !== usuario)

      notifySuccess('Usuario eliminado correctamente')
      await listar()

    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    usuarios,
    loading,
    filtros,
    listar,
    crear,
    editar,
    eliminar,
    buscarConDebounce
  }
}