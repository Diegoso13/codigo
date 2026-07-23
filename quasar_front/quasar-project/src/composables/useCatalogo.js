import { useCrud } from 'src/composables/useCRUD'
import {direccionService,tipoService,cecoService,codigocecoService, sedeService,campanaService,cliente2Service} from  'src/services/catalogoService'

////////////DIRECCION///////////////
export function useDireccion() {
  const crud = useCrud(direccionService, {
    msgCrear: 'Dirección creada correctamente',
    msgEditar: 'Dirección actualizada correctamente',
    msgEliminar: 'Dirección eliminada correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    direcciones: crud.items,
    ...crud
  }
}

////////////TIPO///////////////
export function useTipo() {
  const crud = useCrud(tipoService, {
    msgCrear: 'Tipo creado correctamente',
    msgEditar: 'Tipo actualizado correctamente',
    msgEliminar: 'Tipo eliminado correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    tipos: crud.items,
    ...crud
  }
}

////////////CECO///////////////
export function useCeco() {
  const crud = useCrud(cecoService, {
    msgCrear: 'CECO creado correctamente',
    msgEditar: 'CECO actualizado correctamente',
    msgEliminar: 'CECO eliminado correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    cecos: crud.items,
    ...crud
  }
}

////////////CODIGOCECO///////////////
export function useCodigoCeco() {
  const crud = useCrud(codigocecoService, {
    msgCrear: 'Código CECO creado correctamente',
    msgEditar: 'Código CECO actualizado correctamente',
    msgEliminar: 'Código CECO eliminado correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    codigosCeco: crud.items,
    ...crud
  }
}

////////////SEDE///////////////
export function useSede() {
  const crud = useCrud(sedeService, {
    msgCrear: 'Sede creada correctamente',
    msgEditar: 'Sede actualizada correctamente',
    msgEliminar: 'Sede eliminada correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    sedes: crud.items,
    ...crud
  }
}

////////////CLIENTE2///////////////
export function useCliente2() {
  const crud = useCrud(cliente2Service, {
    msgCrear: 'Cliente2 creado correctamente',
    msgEditar: 'Cliente2 actualizado correctamente',
    msgEliminar: 'Cliente2 eliminado correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    clientes2: crud.items,
    ...crud
  }
}

////////////CAMPAÑA///////////////
export function useCampana() {
  const crud = useCrud(campanaService, {
    msgCrear: 'Campaña creada correctamente',
    msgEditar: 'Campaña actualizada correctamente',
    msgEliminar: 'Campaña eliminada correctamente',
    refrescarDespuesEliminar: true
  })

  return {
    campanas: crud.items,
    ...crud
  }
}
    
