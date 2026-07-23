import { api } from 'boot/axios'

/**
 * Función estandarizada para buscar equipos en los q-select de Quasar.
 * @param {String} val - El texto que el usuario escribe.
 * @param {Function} update - La función de Quasar para actualizar opciones.
 * @param {Ref} equiposRef - La referencia (.value) donde se guardan los resultados.
 */
export async function buscarEquiposUtil(val, update, equiposRef) {
  // 1. Validación mínima de caracteres
  if (val.length < 2) {
    update(() => {
      equiposRef.value = []
    })
    return
  }

  try {
    // 2. Llamada a la nueva ruta que configuramos en el backend
    const res = await api.get('busqueda/select/', { params: { q: val } })

    // 3. Actualización de las opciones del select
    update(() => {
      equiposRef.value = res.data
    })
  } catch (error) {
    console.error('Error buscando equipos:', error)
    update(() => {
      equiposRef.value = []
    })
  }
}
