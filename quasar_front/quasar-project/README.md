# LOLIC Frontend

Frontend del sistema LOLIC para la gestion de licencias, extensiones, usuarios, catalogos, equipos y agenda. El proyecto esta construido con Vue 3, Quasar Framework y Vite.

## Requisitos previos

Antes de clonar y ejecutar el proyecto, instala:

- Git.
- Node.js compatible con el proyecto: 20, 22, 24, 26 o 28.
- npm 6.13.4 o superior.
- Backend/API del proyecto ejecutandose en `http://127.0.0.1:8000/api/` o `http://localhost:8000/api/`.

La lista simple de paquetes y versiones esta en [REQUERIMIENTOS.txt](./REQUERIMIENTOS.txt).

## Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd quasar-project
```

Reemplaza `<URL_DEL_REPOSITORIO>` por la URL real del repositorio.

## Instalar dependencias

Este repositorio incluye `package-lock.json`, por lo que se recomienda usar npm:

```bash
npm install
```

No es necesario subir ni copiar la carpeta `node_modules`; se genera automaticamente con el comando anterior.

## Ejecutar en desarrollo

```bash
npm run dev
```

Quasar abrira el navegador automaticamente. Si no se abre, revisa la URL que aparezca en la terminal, normalmente similar a:

```text
http://localhost:9000/
```

## Configuracion de API

La instancia principal de Axios esta en:

```text
src/boot/axios.js
```

Actualmente usa:

```text
http://127.0.0.1:8000/api/
```

Algunos modulos tambien llaman directamente a `http://localhost:8000/api/`. Por eso, antes de probar el frontend, confirma que el backend este activo en el puerto `8000` y que permita peticiones desde el origen del frontend.

## Scripts disponibles

```bash
npm run dev
```

Inicia el servidor de desarrollo.

```bash
npm run build
```

Genera la version de produccion en la carpeta `dist`.

```bash
npm run lint
```

Ejecuta ESLint sobre archivos JavaScript y Vue.

```bash
npm run format
```

Formatea el codigo con Prettier.

```bash
npm test
```

Ejecuta el script de pruebas configurado. Actualmente no hay pruebas automatizadas definidas.

## Estructura principal

- `src/pages`: pantallas del sistema.
- `src/layouts`: layouts generales de la aplicacion.
- `src/router`: rutas y control de navegacion.
- `src/boot/axios.js`: configuracion de Axios e interceptores de sesion.
- `src/services`: servicios para consumir endpoints del backend.
- `quasar.config.js`: configuracion principal de Quasar.

## Flujo recomendado despues de clonar

1. Clonar el repositorio.
2. Entrar a la carpeta del proyecto.
3. Ejecutar `npm install`.
4. Levantar el backend en `http://127.0.0.1:8000/api/`.
5. Ejecutar `npm run dev`.
6. Iniciar sesion con un usuario valido del backend.

## Solucion de problemas comunes

- Si aparece un error de dependencias, elimina `node_modules` y ejecuta nuevamente `npm install`.
- Si el login o las consultas fallan, valida que el backend este encendido en el puerto `8000`.
- Si hay errores CORS, revisa la configuracion del backend para permitir el origen del servidor Quasar.
- Si Quasar no se reconoce como comando global, usa siempre los scripts de npm, por ejemplo `npm run dev`.
