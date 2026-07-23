import {api} from 'src/boot/axios'

export const movimientosService = {

  listar(params = {}) {
    return api.get('/extensiones/movimientos/', { params })
  }

}
