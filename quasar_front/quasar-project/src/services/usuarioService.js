import { api } from 'src/boot/axios'

export const usuarioService = {

  listar(params = {}) {
    return api.get('/extensiones/usuario/', { params })
  },

  crear(payload){
    return api.post('/extensiones/usuario/', payload)
  },

  editar(usuario, payload) {
    return api.put(`/extensiones/usuario/${usuario}/`, payload)
  },

  eliminar(usuario) {
    return api.delete(`/extensiones/usuario/${usuario}/`)
  }

    
}