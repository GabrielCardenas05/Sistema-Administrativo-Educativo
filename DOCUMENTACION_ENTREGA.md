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
- Gestion de usuarios.
- Validaciones de negocio para inscripciones.
- Auditoria basica de acciones administrativas.
- Scripts SQL para crear, actualizar y poblar la base de datos.
- Frontend con dashboard y navegacion por modulos.

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

En usuarios se valida:

- Que los roles asignados existan antes de guardar.
- Que las operaciones criticas queden protegidas por autenticacion y permisos.

En auditoria:

- Se registran acciones administrativas sobre alumnos, docentes, carreras, materias, inscripciones y usuarios.
- La auditoria es de apoyo para trazabilidad y no bloquea la operacion principal si ocurre un error al registrar el log.

## Relacion con los problemas originales

| Problema original | Respuesta del sistema |
| --- | --- |
| Altas academicas | Modulos de alumnos, docentes, carreras, materias e inscripciones |
| Cambios de materia | Gestion de inscripciones y estados |
| Bajas | Estados en registros academicos |
| Falta de permisos | Autenticacion JWT y roles |
| Materias fuera de carrera/especialidad | Validacion de carrera y semestre al inscribir |
| Cupos incorrectos | Validacion de cupo antes de confirmar inscripcion |
| Datos inconsistentes | Llaves foraneas y validaciones de negocio |
| Sin trazabilidad | Tabla de logs de auditoria |

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
