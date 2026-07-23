import { api } from 'boot/axios'

// SOFTWARE
export async function obtenerSoftware() {
  const response = await api.get('catalogos/software/')

  return response.data
}

// SEDES
export async function obtenerSedes() {
  const response = await api.get('catalogos/sedes/')

  return response.data
}

// CIUDADES
export async function obtenerCiudades() {
  const response = await api.get('catalogos/ciudades/')

  return response.data
}

// PROPIETARIOS
export async function obtenerPropietarios() {
  const response = await api.get('catalogos/propietarios/')

  return response.data
}
