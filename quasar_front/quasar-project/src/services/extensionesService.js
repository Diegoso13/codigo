import { api } from 'src/boot/axios'


export const extensionesService = {

  listar(params = {}) {
    return api.get('/extensiones/extensiones/', { params })
  },
  asignar(payload){
    return api.patch('/extensiones/extensiones/asignar/', payload)
  },
  reasignar(payload) {
    return api.patch(`/extensiones/extensiones/reasignar/`, payload)
  },
  liberar(payload) {
    return api.patch(`/extensiones/extensiones/liberar/`, payload)
  },
  trasladarModificar(payload) {
    return api.patch('/extensiones/extensiones/trasladar_modificar/', payload)
  },
  exportar() {
    return api.get('/extensiones/extensiones/export-excel/', {responseType: 'arraybuffer'})
  }
}