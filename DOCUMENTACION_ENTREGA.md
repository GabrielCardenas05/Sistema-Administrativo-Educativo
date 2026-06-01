# Sistema Administrativo Educativo - Documentacion de Entrega

## Objetivo del proyecto

El sistema atiende el caso de un sistema academico con problemas de calidad en altas, cambios de materia, bajas, validacion de cupos, integridad de datos, permisos y trazabilidad.

La aplicacion permite administrar alumnos, docentes, carreras, materias, inscripciones y usuarios desde una interfaz web, con autenticacion por JWT y control de roles.

## Estado actual

El proyecto queda listo para presentacion funcional con los siguientes puntos cubiertos:

- Autenticacion de usuarios con JWT.
- Roles principales: ADMINISTRADOR, ADMINISTRATIVO, DOCENTE y ALUMNO.
- Gestion de alumnos.
- Gestion de docentes.
- Gestion de carreras.
- Gestion de materias.
- Gestion de inscripciones.
- Consulta y administracion de pagos asociados a inscripciones.
- Inscripcion de alumnos a materias de su semestre con pago simulado y comprobante.
- Tickets de soporte para errores del sistema, materias incorrectas y pagos no reflejados.
- Gestion de usuarios.
- Validaciones de negocio para inscripciones.
- Auditoria basica de acciones administrativas con pantalla de bitacora.
- CHECK constraints en base de datos para estados, cupos, semestres, pagos y tickets.
- Scripts SQL para crear, actualizar y poblar la base de datos.
- Frontend con dashboard y navegacion por modulos.
- Conexion a BD con pooling de pyodbc y timeout configurable.

## Estructura del proyecto

```text
backend/
  main.py                 Punto de entrada de Flask
  config.py               Configuracion de base de datos y JWT
  database.py             Conexion a SQL Server
  routes/                 Endpoints REST
  repositories/           Acceso a datos y reglas de persistencia
  services/               Logica de autenticacion
  utils/                  Seguridad, respuestas y decoradores

frontend/
  index.html              Login
  pages/                  Pantallas internas del sistema
  js/api.js               Cliente para consumir el backend
  js/layout.js            Layout, sidebar, header y navegacion
  js/ui.js                Utilidades visuales
  css/custom.css          Estilos personalizados

BD/
  Crear_BD_Final.sql      Script completo de estructura de BD
  Actualizar_BD.sql       Script de actualizacion para BD existente
  crear admin.sql         Usuario administrador de prueba
  poblar bd.sql           Datos de ejemplo para demostracion
```

## Requisitos

- Python 3.10 o superior.
- SQL Server.
- Navegador web.
- Dependencias de Python indicadas en `backend/requirements.txt`.

## Configuracion del backend

Crear el archivo `backend/.env` tomando como base `backend/.env.example`.

Variables principales:

```env
DB_SERVER=localhost
DB_NAME=SistemaAdministrativoEducativo
DB_USER=sa
DB_PASSWORD=tu_password
DB_TIMEOUT_SECONDS=5
JWT_SECRET_KEY=tu_llave_secreta
FLASK_DEBUG=0
FLASK_HOST=127.0.0.1
```

Instalar dependencias:

```powershell
cd backend
pip install -r requirements.txt
```

Ejecutar backend:

```powershell
python main.py
```

El backend queda disponible en:

```text
http://127.0.0.1:5000
```

Endpoint de verificacion:

```text
GET http://127.0.0.1:5000/api/health
```

## Configuracion de base de datos

Para una instalacion limpia:

1. Ejecutar `BD/Crear_BD_Final.sql`.
2. Ejecutar `BD/crear admin.sql`.
3. Ejecutar `BD/poblar bd.sql`.

Para actualizar una base ya existente:

1. Ejecutar `BD/Actualizar_BD.sql`.
2. Ejecutar los scripts de datos que hagan falta.

Usuario de demostracion:

```text
Usuario: Admin
Password: Admin123
Rol: ADMINISTRADOR
```

## Ejecucion del frontend

Abrir el login desde:

```text
frontend/index.html
```

Tambien se puede servir la carpeta `frontend` con un servidor estatico simple.

Ejemplo:

```powershell
cd frontend
python -m http.server 8000
```

Despues abrir:

```text
http://localhost:8000
```

## Modulos disponibles

- Dashboard: resumen general y accesos rapidos.
- Alumnos: alta, consulta, actualizacion y administracion de alumnos.
- Docentes: alta, consulta, actualizacion y administracion de docentes.
- Carreras: administracion de carreras.
- Materias: administracion de materias, cupos, semestre y carrera.
- Inscripciones: registro y control de materias inscritas por alumno.
- Pagos: registro y actualizacion de pagos por inscripcion.
- Mis pagos: vista de alumno con comprobantes y estado actual de sus pagos.
- Tickets: reportes de pagos no reflejados, materias incorrectas y errores del sistema.
- Bitacora: consulta de logs de auditoria.
- Usuarios: administracion de cuentas y roles.
- Mi Perfil: vista orientada al alumno.

## Validaciones implementadas

En inscripciones se valida:

- Que el alumno exista.
- Que el alumno este activo.
- Que la materia exista.
- Que la materia este activa.
- Que la materia pertenezca a la carrera del alumno.
- Que la materia corresponda al semestre/grado del alumno.
- Que el cupo disponible no este lleno.
- Que el alumno no consulte inscripciones ajenas cuando usa rol ALUMNO.
- Que las bajas tengan un flujo formal con estado `BAJA`, motivo y fecha de baja.
- Que el alumno solo pueda inscribirse desde la interfaz a materias de su carrera y semestre.

En usuarios se valida:

- Que los roles asignados existan antes de guardar.
- Que las operaciones criticas queden protegidas por autenticacion y permisos.

En auditoria:

- Se registran acciones administrativas sobre alumnos, docentes, carreras, materias, inscripciones y usuarios.
- Los administradores y administrativos pueden consultar la bitacora desde el frontend.
- La auditoria es de apoyo para trazabilidad y no bloquea la operacion principal si ocurre un error al registrar el log.

En pagos:

- Los administradores y administrativos pueden registrar y actualizar pagos.
- Los alumnos pueden pagar una inscripcion con tarjeta simulada desde el modulo de inscripciones.
- La tarjeta simulada exige numero con formato valido, titular, CVV y fecha de expiracion vigente.
- El sistema no guarda numero completo de tarjeta ni CVV; solo registra los ultimos 4 digitos y el folio.
- Cada pago genera referencia/comprobante consultable desde la pestaña de pagos del alumno.
- El monto debe ser mayor a cero.
- El estado del pago se limita a `PENDIENTE`, `PAGADO` o `RECHAZADO`.

En tickets:

- Los usuarios autenticados pueden generar tickets de soporte.
- Los alumnos solo pueden reportar inscripciones que les pertenecen.
- Los administradores y administrativos pueden ver todos los tickets y cambiar su estatus.
- Los reportes contemplan pago no reflejado, materia incorrecta, error del sistema u otro problema.

En base de datos:

- `alumnos.semestre` y `materias.semestre` quedan limitados a valores validos de 1 a 10.
- `materias.cupo` queda limitado a valores positivos.
- Los estados de alumnos, inscripciones, pagos y tickets quedan restringidos por `CHECK`.
- Las bajas de inscripcion exigen `motivo_baja` y `fecha_baja`.

En concurrencia y carga:

- El sistema usa JWT sin estado de sesion en servidor, por lo que cada peticion se valida con el token del usuario actual.
- Las consultas usan parametros SQL, no concatenacion de datos del usuario.
- Las vistas de alumno consultan su perfil por `id_usuario` del token y no por datos enviados desde el navegador.
- La vista de docente usa una consulta general de inscripciones en lugar de una llamada por cada alumno.
- La conexion a SQL Server usa pooling de pyodbc y timeout configurable con `DB_TIMEOUT_SECONDS`.
- Para una entrega productiva se recomienda ejecutar Flask detras de un servidor WSGI y no con el servidor de desarrollo.

## Relacion con los problemas originales

| Problema original | Respuesta del sistema |
| --- | --- |
| Altas academicas | Modulos de alumnos, docentes, carreras, materias e inscripciones |
| Cambios de materia | Gestion de inscripciones y estados |
| Bajas | Flujo formal de baja con motivo y fecha |
| Falta de permisos | Autenticacion JWT y roles |
| Materias fuera de carrera/especialidad | Validacion de carrera y semestre al inscribir |
| Cupos incorrectos | Validacion de cupo antes de confirmar inscripcion |
| Datos inconsistentes | Llaves foraneas, CHECK constraints y validaciones de negocio |
| Sin trazabilidad | Tabla y pantalla de bitacora de auditoria |
| Pago no reflejado | Administracion de pagos, comprobantes, estado de pagos en inscripciones y tickets de soporte |
| Errores reportados por usuarios | Modulo de tickets con seguimiento de estatus |

## Notas para presentacion

- Iniciar SQL Server y verificar que la base de datos exista.
- Ejecutar el backend antes de abrir el frontend.
- Entrar con `Admin / Admin123`.
- Mostrar primero el dashboard.
- Recorrer alumnos, docentes, carreras, materias e inscripciones.
- Enfatizar que las validaciones buscan corregir los errores descritos en el caso original.

## Limitaciones conocidas

- La aplicacion esta preparada para demostracion academica, no para produccion.
- La llave JWT debe manejarse por `.env` y no subirse al repositorio.
- Se recomienda ampliar pruebas automatizadas si el proyecto continua despues de la entrega.
