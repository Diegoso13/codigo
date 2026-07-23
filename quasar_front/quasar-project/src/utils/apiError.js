export function getApiErrorMessage(e) {
  const err = e

  const data = err?.response?.data

  if (!data) return err?.message ?? 'Error inesperado'

  if (typeof data === 'object' && data !== null) {
    const messages = []

    for (const key in data) {
      const value = data[key]

      if (Array.isArray(value)) {
        messages.push(`${key}: ${value.join(', ')}`)
      } else {
        messages.push(`${key}: ${String(value)}`)
      }
    }

    if (messages.length) return messages.join(' | ')
  }

  if (typeof data === 'string') {
    return data
  }

  return 'Error en la solicitud'
}