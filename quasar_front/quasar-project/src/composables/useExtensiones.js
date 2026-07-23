import { ref } from 'vue'
import { extensionesService } from 'src/services/extensionesService'
import { notifyError, notifySuccess } from 'src/utils/notify'

export function useExtensiones() {
  const extensiones = ref([])
  const loading = ref(false)

  const filtros = ref({
    search: '',
    estado: null,
    tipo: null,
  })

  let timeout = null

  // LISTAR
  const listar = async (params = {}) => {
    loading.value = true

    try {
      const { data } = await extensionesService.listar({
        search: filtros.value.search || null,
        estado: filtros.value.estado || null,
        tipo: filtros.value.tipo || null,
        ...params,
      })

      extensiones.value = Array.isArray(data) ? data : (data.results ?? [])
    } catch (e) {
      notifyError(e)
    } finally {
      loading.value = false
    }
  }

  // DEBOUNCE SEARCH
  const buscarConDebounce = () => {
    clearTimeout(timeout)

    timeout = setTimeout(() => {
      listar()
    }, 400)
  }

  // ASIGNAR
  const asignar = async (payload) => {
    loading.value = true

    try {
      const { data } = await extensionesService.asignar(payload)

      notifySuccess('Extensión asignada correctamente')

      return data
    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  // REASIGNAR
  const reasignar = async (payload) => {
    loading.value = true

    try {
      const { data } = await extensionesService.reasignar(payload)

      notifySuccess('Extensión reasignada correctamente')

      return data
    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  // LIBERAR
  const liberar = async (payload) => {
    loading.value = true

    try {
      const { data } = await extensionesService.liberar(payload)

      notifySuccess('Extensión liberada correctamente')

      return data
    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  // TRASLADAR MODIFICANDO
  const trasladarModificar = async (payload) => {
    loading.value = true

    try {
      const { data } = await extensionesService.trasladarModificar(payload)
      notifySuccess('Traslado modificado correctamente')
      return data
    } catch (e) {
      notifyError(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  // EXPORTAR EXCEL
  const exportar = async () => {
    try {
      const response = await extensionesService.exportar()

      const blob = new Blob([response.data], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      })

      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'extensiones.xlsx'

      document.body.appendChild(link)
      link.click()

      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (e) {
      console.error(e)
      notifyError(e)
    }
  }

  return {
    extensiones,
    loading,
    filtros,
    listar,
    buscarConDebounce,
    asignar,
    reasignar,
    liberar,
    trasladarModificar,
    exportar,
  }
}
