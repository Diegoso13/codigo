import { ref } from 'vue'
import { movimientosService } from 'src/services/movimientoService'

export function useMovimientos() {

  const movimientos = ref([])
  const loading = ref(false)
  const error = ref(null)

  const filtros = ref({
    search: '',
    tipo_movimiento: null,
    marca: null,
    usuario: null,
    extension: null,
    ticket: null,
    ordering: '-fecha'
  })

  async function listar(extraParams = {}) {
    loading.value = true
    error.value = null

    try {
      const params = {
        ...filtros.value,
        ...extraParams
      }

      const { data } = await movimientosService.listar(params)

      movimientos.value = data

    } catch (e) {
      error.value = e
      console.error('Error cargando movimientos:', e)

    } finally {
      loading.value = false
    }
  }

  function limpiarFiltros() {
    filtros.value = {
      search: '',
      tipo_movimiento: null,
      marca: null,
      usuario: null,
      extension: null,
      ticket: null,
      ordering: '-fecha'
    }
  }

  return {
    movimientos,
    loading,
    error,
    filtros,
    listar,
    limpiarFiltros
  }
}