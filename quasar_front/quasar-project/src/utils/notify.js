import { Notify } from 'quasar'
import { getApiErrorMessage } from 'src/utils/apiError'

export function notifyError(e) {
  Notify.create({
    type: 'negative',
    message: getApiErrorMessage(e),
    position: 'top', // 👈 aquí
    multiLine: true,
    timeout: 5000
  })
}

export function notifySuccess(message) {
  Notify.create({
    type: 'positive',
    message,
    position: 'top', // 👈 aquí
  })
}

export function notifyWarning(message) {
  Notify.create({
    type: 'warning',
    message,
    position: 'top', // 👈 aquí
  })
}