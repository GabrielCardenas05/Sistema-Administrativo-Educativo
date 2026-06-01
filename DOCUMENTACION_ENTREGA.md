# Sistema Administrativo Educativo - Documentacion de Entrega

## Objetivo del proyecto

El sistema atiende el caso de un sistema academico universitario con problemas de calidad en altas, cambios de materia, bajas, validacion de cupos, pagos, integridad de datos, permisos, reportes y trazabilidad.

La aplicacion permite administrar alumnos, docentes, carreras, materias, inscripciones, pagos, tickets y usuarios desde una interfaz web, con autenticacion JWT, control por roles y validaciones en frontend, backend y base de datos.

## Relacion con la rubrica

La entrega se organiza para cubrir los criterios de evaluacion:

| Criterio de rubrica | Evidencia del proyecto |
| --- | --- |
| Calidad de requerimientos | `Tabla de requerimientos ACADEMICO.xlsx`, hoja `Requerimientos`. Cada fila liga problema, requisito, pantalla, backend, BD, query y evidencia visual. |
| Calidad de base de datos | Scripts `BD/Crear_BD_Final.sql`, `BD/Actualizar_BD.sql`, diagrama ER/captura de tablas, FK, UNIQUE, CHECK e indices. |
| Diseno y arquitectura | Separacion `frontend/pages`, `frontend/js`, `backend/routes`, `backend/repositories`, `backend/services`, `backend/utils` y `BD`. |
| Experiencia de usuario | Dashboard por rol, navegacion lateral, formularios con mensajes, confirmaciones y pantallas de pagos/tickets/bitacora. |
| Evidencia de funcionamiento | Capturas indicadas en `DOCUMENTO_WORD_HORIZONTAL_ENTREGA.md` y hoja `Evidencias` del Excel. |

## Estado actual

El proyecto queda listo para presentacion funcional con los siguientes puntos cubiertos:

- Autenticacion de usuarios con JWT.
- Roles principales: ADMINISTRADOR, ADMINISTRATIVO, DOCENTE y ALUMNO.
- Gestion de alumnos, docentes, carreras, materias, inscripciones, pagos, tickets, usuarios y bitacora.
- Asignacion de docentes a materias mediante relacion `materia_docente`.
- Inscripcion de alumnos a materias de su carrera y semestre.
- Pago simulado con tarjeta, validacion de numero, titular, CVV y expiracion.
- Comprobante de pago consultable por el alumno en `Pagos / Mis pagos`.
- Tickets de soporte para errores del sistema, materias incorrectas y pagos no reflejados.
- Flujo formal de baja de inscripcion con estado `BAJA`, motivo y fecha.
- Auditoria de acciones administrativas en `logs_auditoria` y pantalla `Bitacora`.
- CHECK constraints para estados, prioridad, tipo de ticket, cupo positivo, semestre valido y pagos.
- Scripts SQL para crear, actualizar y poblar la base de datos.
- Scripts demo para materias/docentes sin alumnos y alumnos de semestres altos.
- Frontend con dashboard y navegacion por modulos segun rol.
- Conexion a SQL Server con pooling de pyodbc y timeout configurable.

## Estructura del proyecto

```text
backend/
  main.py                 Punto de entrada de Flask
  config.py               Configuracion de BD, JWT y CORS
  database.py             Conexion a SQL Server
  routes/                 Endpoints REST por modulo
  repositories/           Acceso a datos y validaciones de persistencia
  services/               Logica de autenticacion
  utils/                  Seguridad, respuestas, auditoria y decoradores

frontend/
  index.html              Login
  pages/                  Pantallas internas del sistema
  js/api.js               Cliente HTTP del backend
  js/layout.js            Layout, sidebar, header y permisos visuales
  js/ui.js                Toasts, confirmaciones y utilidades visuales
  css/custom.css          Estilos personalizados

BD/
  Crear_BD_Final.sql                       Script completo de estructura
  Actualizar_BD.sql                        Script idempotente para BD existente
  crear admin.sql                          Usuario administrador de prueba
  poblar bd.sql                            Datos base para demostracion
  agregar_materias_docentes_demo.sql       Mas materias y docentes sin alumnos inscritos
  agregar_alumnos_altos_semestres_demo.sql Alumnos demo de semestres altos
```

## Requisitos

- Python 3.10 o superior.
- SQL Server.
- Navegador web.
- Dependencias de Python indicadas en `backend/requirements.txt`.

## Comandos de ejecucion

Backend:

```powershell
cd "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo"
$env:JWT_SECRET_KEY="SistemaAdministrativoEscolarJWT2026Super"
$env:DB_SERVER="localhost"
$env:DB_NAME="CalidadYPruebas_SE"
.\.venv\Scripts\python.exe backend\main.py
```

Frontend:

```powershell
cd "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\frontend"
python -m http.server 8000
```

Despues abrir:

```text
http://localhost:8000
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
4. Ejecutar `BD/agregar_materias_docentes_demo.sql`.
5. Ejecutar `BD/agregar_alumnos_altos_semestres_demo.sql`.

Para actualizar una base ya existente:

1. Ejecutar `BD/Actualizar_BD.sql`.
2. Ejecutar `BD/agregar_materias_docentes_demo.sql`.
3. Ejecutar `BD/agregar_alumnos_altos_semestres_demo.sql`.

Ejemplo con `sqlcmd`:

```powershell
sqlcmd -S localhost -d CalidadYPruebas_SE -E -i "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\BD\Actualizar_BD.sql"
sqlcmd -S localhost -d CalidadYPruebas_SE -E -i "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\BD\agregar_materias_docentes_demo.sql"
sqlcmd -S localhost -d CalidadYPruebas_SE -E -i "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\BD\agregar_alumnos_altos_semestres_demo.sql"
```

## Usuarios demo

| Usuario | Password | Rol | Uso sugerido |
| --- | --- | --- | --- |
| Admin | Admin123 | ADMINISTRADOR | Mostrar dashboard completo, CRUD, pagos, tickets y bitacora. |
| Alumno1 | Admin123 | ALUMNO | Mostrar inscripcion, pago simulado, comprobante, mis pagos y tickets. |
| Docente1 | Admin123 | DOCENTE | Mostrar vista de consulta de alumnos/materias. |
| AlumnoSis4 | Admin123 | ALUMNO | Validar materias de Sistemas de semestre alto. |
| AlumnoCom4 | Admin123 | ALUMNO | Validar materias de Comunicacion de semestre alto. |
| AlumnoAdm4 | Admin123 | ALUMNO | Validar materias de Administracion de semestre alto. |

## Modulos disponibles

- Dashboard: resumen general y accesos rapidos segun rol.
- Alumnos: alta, consulta, actualizacion y administracion de alumnos.
- Docentes: alta, consulta, actualizacion y administracion de docentes.
- Carreras: administracion de carreras.
- Materias: administracion de materias, cupos, semestre, carrera y docentes asignados.
- Inscripciones: registro, consulta, baja formal y control de materias inscritas.
- Pagos: administracion de pagos por inscripcion para admin/administrativo.
- Mis pagos: vista de alumno con comprobantes y estado actual de sus pagos.
- Tickets: reportes de pagos no reflejados, materias incorrectas y errores del sistema.
- Bitacora: consulta de logs de auditoria.
- Usuarios: administracion de cuentas y roles.
- Mi Perfil: vista orientada al alumno.

## Validaciones implementadas

En inscripciones:

- El alumno debe existir y estar activo.
- La materia debe existir y estar activa.
- La materia debe pertenecer a la carrera del alumno.
- La materia debe corresponder al semestre/grado del alumno.
- El cupo disponible se valida antes de confirmar.
- Se bloquea la inscripcion duplicada en la misma materia y periodo.
- Un alumno no puede consultar inscripciones ajenas.
- El alumno solo ve materias de su propia carrera desde backend.
- El alumno solo puede inscribirse desde interfaz a materias de su carrera y semestre.
- La baja exige estado `BAJA`, motivo y fecha.

En pagos:

- El alumno puede pagar una inscripcion con tarjeta simulada.
- Se valida numero de tarjeta, titular, CVV y fecha de expiracion vigente.
- El sistema no guarda numero completo de tarjeta ni CVV.
- Se registra metodo, titular, ultimos 4 digitos, folio/referencia, concepto y comprobante.
- El monto debe ser mayor a cero.
- El estado queda limitado a `PENDIENTE`, `PAGADO` o `RECHAZADO`.

En tickets:

- Los usuarios autenticados pueden generar tickets.
- Los alumnos solo pueden reportar inscripciones propias.
- Los tipos quedan limitados a `MATERIA_INCORRECTA`, `PAGO_NO_REFLEJADO`, `ERROR_SISTEMA` u `OTRO`.
- El estatus queda limitado a `ABIERTO`, `EN_REVISION`, `RESUELTO` o `CERRADO`.
- La prioridad queda limitada a `BAJA`, `MEDIA` o `ALTA`.

En seguridad y auditoria:

- Las rutas criticas usan `require_auth` y `require_role`.
- Los roles asignados deben existir antes de guardar.
- Las acciones administrativas se registran en `logs_auditoria`.
- La bitacora se consulta desde el frontend por administradores/administrativos.

En base de datos:

- `alumnos.semestre` y `materias.semestre` se limitan a valores 1 a 10.
- `materias.cupo` debe ser positivo.
- Los estados de alumnos, materias, carreras, inscripciones, pagos y tickets se restringen por `CHECK`.
- Existen FK para mantener relaciones entre usuarios, roles, alumnos, docentes, carreras, materias, inscripciones, pagos y tickets.
- Existen UNIQUE para evitar usuarios, matriculas, CURP, claves de materia e inscripciones duplicadas.
- `materia_docente` permite registrar docentes que imparten materias sin crear inscripciones de alumnos.

En concurrencia y carga:

- El sistema usa JWT sin estado de sesion en servidor; cada peticion se valida con el token actual.
- Las consultas usan parametros SQL en vez de concatenar datos del usuario.
- Las vistas de alumno consultan el perfil por `id_usuario` del token, no por un dato editable en el navegador.
- El backend vuelve a validar carrera/semestre/cupo aunque el frontend ya filtre.
- La conexion a SQL Server usa pooling de pyodbc y `DB_TIMEOUT_SECONDS`.
- Para produccion se recomienda ejecutar Flask con WSGI y pruebas de carga formales.

## Relacion con los problemas originales

| Problema original | Respuesta del sistema |
| --- | --- |
| Altas academicas | Modulos de alumnos, docentes, carreras, materias e inscripciones. |
| Cambios de materia | Gestion de inscripciones, estados y validaciones. |
| Bajas inexistentes | Flujo formal de baja con motivo y fecha. |
| Falta de permisos | Autenticacion JWT, roles y decoradores de autorizacion. |
| Materias fuera de carrera/especialidad | Filtro y validacion de carrera y semestre. |
| Cupos incorrectos | Validacion de cupo antes de confirmar inscripcion. |
| Datos inconsistentes | FK, UNIQUE, CHECK y validaciones de negocio. |
| Sin trazabilidad | `logs_auditoria` y pantalla `Bitacora`. |
| Pago no reflejado | Pagos, comprobantes, estado de pago en inscripciones y tickets. |
| Reportes administrativos no confiables | Consultas centralizadas desde la BD, sin datos inventados en frontend. |
| Alta demanda con datos cruzados | Uso de token por usuario, consultas parametrizadas y validacion server-side. |

## Evidencias sugeridas

Las capturas exactas estan listadas en `DOCUMENTO_WORD_HORIZONTAL_ENTREGA.md` y en la hoja `Evidencias` de `Tabla de requerimientos ACADEMICO.xlsx`.

Capturas minimas para entregar:

1. Login y dashboard de administrador.
2. Diagrama ER o captura de tablas principales.
3. Tabla de requerimientos desde Excel.
4. Pantalla Materias con carrera, semestre y docentes.
5. Alumno viendo solo materias de su carrera/semestre.
6. Inscripcion de alumno y pago simulado.
7. Comprobante de pago.
8. Mis pagos con estado actual.
9. Tickets de soporte.
10. Bitacora de auditoria.
11. Evidencia SQL de constraints/scripts ejecutados.

## Limitaciones conocidas

- La aplicacion esta preparada para demostracion academica, no para produccion.
- La llave JWT debe manejarse por `.env` y no subirse en repositorios publicos.
- El pago es simulado; valida formato de tarjeta pero no conecta con una pasarela real.
- La base actual no incluye una tabla formal de horarios/salones. Si una materia no tiene ese dato, la interfaz muestra `No registrado`.
- La proteccion para alta demanda esta mitigada por validaciones y consultas por usuario, pero no sustituye pruebas de carga con usuarios concurrentes reales.
- Se recomienda ampliar pruebas automatizadas si el proyecto continua despues de la entrega.

## Conclusiones de calidad

El proyecto corrige los puntos principales del caso original al pasar de un sistema con altas basicas y datos inconsistentes a una solucion con validaciones por rol, filtros academicos, control de pagos, soporte, auditoria y restricciones de base de datos.

La calidad total se aborda desde tres niveles: interfaz clara para el usuario, reglas de negocio en backend y restricciones en SQL Server para evitar que los datos queden inconsistentes aunque exista alta demanda o errores de uso.
