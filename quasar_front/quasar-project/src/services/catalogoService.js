import { api } from 'src/boot/axios'

////////////////////////////////////////////////// TIPO //////////////
export const tipoService = {

  listar(params = {}) {
    return api.get('/extensiones/tipo/', { params })
  },
  crear(payload){
    return api.post('/extensiones/tipo/', payload)
  },
  editar(tipo, payload) {
    return api.put(`/extensiones/tipo/${tipo}/`, payload)
  },
  eliminar(tipo) {
    return api.delete(`/extensiones/tipo/${tipo}/`)
  }
}

////////////////////////////////////////////////// DIRECCION //////////////
export const direccionService = {

  listar(params = {}) {
    return api.get('/extensiones/direccion/', { params })
  },
  crear(payload){
    return api.post('/extensiones/direccion/', payload)
  },
  editar(direccion, payload) {
    return api.put(`/extensiones/direccion/${direccion}/`, payload)
  },
  eliminar(direccion) {
    return api.delete(`/extensiones/direccion/${direccion}/`)
  }
}

////////////////////////////////////////////////// CECO //////////////
export const cecoService = {

  listar(params = {}) {
    return api.get('/extensiones/ceco/', { params })
  },
  crear(payload){
    return api.post('/extensiones/ceco/', payload)
  },
  editar(ceco, payload) {
    return api.put(`/extensiones/ceco/${ceco}/`, payload)
  },
  eliminar(ceco) {
    return api.delete(`/extensiones/ceco/${ceco}/`)
  }
}

////////////////////////////////////////////////// CÓDIGO CECO //////////////
export const codigocecoService = {

  listar(params = {}) {
    return api.get('/extensiones/codigoceco/', { params })
  },
  crear(payload){
    return api.post('/extensiones/codigoceco/', payload)
  },
  editar(codigoceco, payload) {
    return api.put(`/extensiones/codigoceco/${codigoceco}/`, payload)
  },
  eliminar(codigoceco) {
    return api.delete(`/extensiones/codigoceco/${codigoceco}/`)
  }
}

////////////////////////////////////////////////// CAMPAÑA //////////////
export const campanaService = {

  listar(params = {}) {
    return api.get('/extensiones/campana/', { params })
  },
  crear(payload){
    return api.post('/extensiones/campana/', payload)
  },
  editar(campana, payload) {
    return api.put(`/extensiones/campana/${campana}/`, payload)
  },
  eliminar(campana) {
    return api.delete(`/extensiones/campana/${campana}/`)
  }
}

////////////////////////////////////////////////// SEDE //////////////
export const sedeService = {

  listar(params = {}) {
    return api.get('/extensiones/sede/', { params })
  },
  crear(payload){
    return api.post('/extensiones/sede/', payload)
  },
  editar(sede, payload) {
    return api.put(`/extensiones/sede/${sede}/`, payload)
  },
  eliminar(sede) {
    return api.delete(`/extensiones/sede/${sede}/`)
  }
}

////////////////////////////////////////////////// CLIENTE2 //////////////
export const cliente2Service = {

  listar(params = {}) {
    return api.get('/extensiones/cliente2/', { params })
  },
  crear(payload){
    return api.post('/extensiones/cliente2/', payload)
  },
  editar(cliente2, payload) {
    return api.put(`/extensiones/cliente2/${cliente2}/`, payload)
  },
  eliminar(cliente2) {
    return api.delete(`/extensiones/cliente2/${cliente2}/`)
  }
}