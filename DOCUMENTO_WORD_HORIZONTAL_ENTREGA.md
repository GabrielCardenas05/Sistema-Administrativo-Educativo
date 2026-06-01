# Texto listo para Word - Formato horizontal

Instruccion rapida antes de pegar:

1. En Word abre un documento nuevo.
2. Ve a `Disposicion > Orientacion > Horizontal`.
3. Usa margenes estrechos.
4. Fuente sugerida: Arial o Aptos 10.5.
5. Copia desde el titulo "Portada" hacia abajo.
6. En cada espacio de captura, borra la instruccion cuando ya pegues la imagen.

---

# Portada

UNIVERSIDAD AUTONOMA DE COAHUILA  
FACULTAD DE SISTEMAS  
CALIDAD Y PRUEBAS DE SOFTWARE  
ENE-JUN 2026  

## Proyecto Ordinario

# Sistema Administrativo Educativo

## Reporte formal de analisis, mejora y evidencia de calidad

Empresa ficticia de aseguramiento de calidad: AulaTest QA  
Sistema evaluado: Sistema Integral de Inscripciones Universitarias  
Equipo: [ESCRIBIR NOMBRE DEL EQUIPO]  
Integrantes: [ESCRIBIR INTEGRANTES]  
Docente: Ing. Mariana Arellano  
Fecha: 01 de junio de 2026  

[ESPACIO PARA LOGOTIPO]
Instruccion: coloca aqui el logo de la empresa ficticia de calidad. Puede ser un logo simple con el texto "AulaTest QA".

---

# 1. Descripcion del giro de la aplicacion

El proyecto corresponde a un sistema administrativo educativo para una institucion universitaria. Su giro principal es la gestion academica: alumnos, docentes, carreras, materias, inscripciones, pagos, tickets de soporte, usuarios y auditoria.

El sistema busca corregir fallas de calidad detectadas en un sistema academico previo, donde existian problemas de inscripciones incorrectas, pagos no reflejados, informacion academica inconsistente, falta de bajas formales, ausencia de trazabilidad y reportes administrativos que no coincidían con los datos reales.

Los usuarios principales son:

- Administrador: gestiona catalogos, usuarios, pagos, tickets y bitacora.
- Administrativo: apoya procesos academicos y administrativos.
- Docente: consulta informacion academica autorizada.
- Alumno: consulta su perfil, materias, inscripciones, pagos y tickets.

---

# 2. Objetivo del sistema

Desarrollar y validar un sistema administrativo educativo que permita controlar la informacion academica con mayor calidad, evitando errores de asignacion de materias, pagos no reflejados, datos duplicados, accesos indebidos y cambios sin trazabilidad.

El sistema implementa validaciones en tres niveles:

- Interfaz: formularios, filtros, mensajes y confirmaciones visibles para el usuario.
- Backend: reglas de negocio, permisos por rol y validaciones antes de guardar.
- Base de datos: llaves primarias, llaves foraneas, UNIQUE, CHECK e indices.

---

# 3. Analisis del sistema sin calidad

El caso original describe un sistema de inscripciones que solo permite altas y cambios de materias en linea, pero no bajas. Durante periodos de alta demanda, algunos alumnos aparecen inscritos en materias que no les corresponden, en materias que ya cursaron o con estados academicos incorrectos. Tambien existen problemas con cupos disponibles, datos personales marcados como incorrectos, pagos no reflejados, reportes administrativos inconsistentes y falta de trazabilidad.

Problemas detectados:

1. El sistema no contempla bajas formales.
2. Alumnos pueden aparecer inscritos en materias que no les corresponden.
3. Materias cursadas, reprobadas o acreditadas pueden mostrarse incorrectamente.
4. Los cupos pueden mostrarse disponibles aunque al confirmar generen error.
5. Datos personales como nombre, telefono, CURP o domicilio pueden marcarse como incorrectos.
6. El pago de ficha o inscripcion no siempre aparece reflejado.
7. Los reportes administrativos no coinciden con la informacion real.
8. No existe trazabilidad de cambios administrativos o academicos.
9. No hay un mecanismo claro de soporte para reportar errores del sistema.
10. Bajo alta demanda existe riesgo de mostrar o cargar datos de otros alumnos.

Impacto general:

Estos problemas afectan la confiabilidad del sistema, la experiencia del usuario, la integridad de la base de datos y la capacidad administrativa para comprobar quien hizo cambios, cuando y por que.

---

# 4. Tabla de requerimientos funcionales

[ESPACIO PARA TABLA DE REQUERIMIENTOS]

Instruccion para llenar este espacio:

1. Abre el archivo `Tabla de requerimientos ACADEMICO.xlsx`.
2. Ve a la hoja `Requerimientos`.
3. Copia la tabla como imagen o toma captura de las columnas principales.
4. Pega aqui la imagen.
5. Si la tabla queda muy grande, pega primero las columnas: ID, PROBLEMA, REQUERIMIENTO, FRONT-END, BACK-END, DATABASE y FRONT VISUAL. Luego agrega otra captura con QUERY si hace falta.

Texto para acompanar la tabla:

La tabla de requerimientos relaciona cada problema del caso con una solucion verificable. Cada fila incluye la necesidad detectada, el comportamiento esperado, la pantalla donde se evidencia, la ruta o validacion de backend, las tablas o restricciones de base de datos involucradas, una consulta SQL de comprobacion y la captura sugerida para comprobar el cumplimiento.

---

# 5. Diseno y arquitectura del sistema

La aplicacion se organiza por capas para separar responsabilidades:

Frontend:

- `frontend/index.html`: pantalla de login.
- `frontend/pages/`: pantallas internas por modulo.
- `frontend/js/api.js`: comunicacion con el backend.
- `frontend/js/layout.js`: menu, header y permisos visuales.
- `frontend/js/ui.js`: toasts, confirmaciones y utilidades.
- `frontend/css/custom.css`: estilos del sistema.

Backend:

- `backend/main.py`: configuracion de Flask y registro de rutas.
- `backend/routes/`: endpoints REST.
- `backend/repositories/`: acceso a datos y reglas de persistencia.
- `backend/services/`: logica de autenticacion.
- `backend/utils/`: seguridad, respuestas, auditoria y decoradores.

Base de datos:

- `BD/Crear_BD_Final.sql`: estructura completa.
- `BD/Actualizar_BD.sql`: actualizacion idempotente de BD existente.
- `BD/poblar bd.sql`: datos base.
- `BD/agregar_materias_docentes_demo.sql`: materias y docentes extra sin alumnos inscritos.
- `BD/agregar_alumnos_altos_semestres_demo.sql`: usuarios alumnos de semestres altos para validacion.

Diagrama de arquitectura:

Usuario en navegador
-> Frontend HTML/CSS/JS
-> API REST Flask
-> Repositorios SQL parametrizados
-> SQL Server
-> Respuesta JSON
-> Interfaz con mensajes, tablas y comprobantes

[ESPACIO PARA CAPTURA O DIAGRAMA DE ARQUITECTURA]
Instruccion: pega una captura del explorador del proyecto mostrando carpetas `backend`, `frontend` y `BD`, o convierte el diagrama textual anterior en una figura.

---

# 6. Diagrama de base de datos

[ESPACIO PARA DIAGRAMA ER]

Instruccion para tomar la captura:

1. Abre SQL Server Management Studio.
2. En la base `CalidadYPruebas_SE`, abre el diagrama o muestra las tablas principales.
3. Deben aparecer, cuando sea posible: usuarios, roles, Usuario_Rol, alumnos, docentes, carreras, materias, materia_docente, periodos, inscripciones, pagos, tickets_soporte y logs_auditoria.
4. Pega la captura en este espacio.

Texto para acompanar el diagrama:

La base de datos corresponde al giro academico del sistema. Las relaciones principales permiten vincular usuarios con roles, alumnos con carreras, materias con carreras y docentes, inscripciones con alumnos/materias/periodos, pagos con inscripciones, tickets con usuarios y la bitacora con acciones administrativas.

La integridad se refuerza mediante:

- Llaves primarias para identificar cada registro.
- Llaves foraneas para evitar relaciones inexistentes.
- UNIQUE para impedir duplicados criticos.
- CHECK para limitar estados, cupos, semestres, tipos de ticket, prioridad y pagos.
- Indices para consultas frecuentes de inscripciones, pagos y tickets.

---

# 7. Script SQL o capturas de tablas

[ESPACIO PARA CAPTURA DE SCRIPT SQL O TABLAS]

Instruccion:

1. Captura la ejecucion de `BD/Actualizar_BD.sql` o `BD/Crear_BD_Final.sql`.
2. Tambien puedes capturar una consulta a `sys.check_constraints` mostrando los CHECK agregados.
3. Pega aqui la evidencia.

Comando usado para actualizar una BD existente:

```powershell
sqlcmd -S localhost -d CalidadYPruebas_SE -E -i "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\BD\Actualizar_BD.sql"
```

Comandos usados para datos demo:

```powershell
sqlcmd -S localhost -d CalidadYPruebas_SE -E -i "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\BD\agregar_materias_docentes_demo.sql"
sqlcmd -S localhost -d CalidadYPruebas_SE -E -i "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\BD\agregar_alumnos_altos_semestres_demo.sql"
```

---

# 8. Evidencia de funcionamiento de la aplicacion

## 8.1 Login y dashboard administrador

[ESPACIO PARA CAPTURA 01]

Instruccion:

1. Ejecuta backend y frontend.
2. Abre `http://localhost:8000`.
3. Inicia sesion con `Admin / Admin123`.
4. Captura el dashboard con el menu lateral completo.

Evidencia esperada:

El administrador debe ver acceso a alumnos, docentes, carreras, materias, inscripciones, pagos, tickets, bitacora y usuarios.

## 8.2 Gestion de materias con carrera, semestre y docentes

[ESPACIO PARA CAPTURA 02]

Instruccion:

1. Inicia sesion como Admin o Docente1.
2. Entra a Materias.
3. Captura los filtros de carrera/semestre y las materias con docentes asignados.

Evidencia esperada:

Las materias deben mostrar clave, nombre, carrera, semestre, cupo, estado y docentes cuando existan.

## 8.3 Alumno viendo solo materias de su carrera y semestre

[ESPACIO PARA CAPTURA 03]

Instruccion:

1. Inicia sesion como `Alumno1 / Admin123`.
2. Entra a Materias o Inscripciones.
3. Captura que solo aparecen materias de su carrera y semestre.
4. Repite, si hay tiempo, con `AlumnoSis4`, `AlumnoCom4` o `AlumnoAdm4` para mostrar semestres altos.

Evidencia esperada:

El alumno no debe ver materias de otra carrera ni de otro semestre.

## 8.4 Inscripcion de alumno

[ESPACIO PARA CAPTURA 04]

Instruccion:

1. Entra como Alumno1.
2. Ve a Inscripciones.
3. Captura la lista de materias disponibles y el boton para inscribirse/pagar.

Evidencia esperada:

La pantalla debe permitir la inscripcion solo a materias validas para el alumno.

## 8.5 Pago simulado y comprobante

[ESPACIO PARA CAPTURA 05]

Instruccion:

1. Desde Inscripciones, elige una materia disponible.
2. Usa el pago simulado con numero de tarjeta, titular, CVV y expiracion vigente.
3. Captura el comprobante que se genera.

Evidencia esperada:

El comprobante debe mostrar folio o referencia, alumno, materia, monto, fecha, estado y ultimos 4 digitos de la tarjeta. El sistema no debe mostrar ni guardar el numero completo ni el CVV.

## 8.6 Mis pagos

[ESPACIO PARA CAPTURA 06]

Instruccion:

1. Con el mismo Alumno1 entra a Pagos/Mis pagos.
2. Captura el listado de pagos y el boton de comprobante.

Evidencia esperada:

El alumno debe ver sus pagos, su estado actual y comprobantes.

## 8.7 Tickets de soporte

[ESPACIO PARA CAPTURA 07]

Instruccion:

1. Entra a Tickets.
2. Crea un ticket de tipo pago no reflejado, materia incorrecta o error del sistema.
3. Captura el listado del ticket creado.
4. Si entras como Admin, captura tambien el cambio de estatus.

Evidencia esperada:

El sistema debe permitir reportar problemas y dar seguimiento administrativo.

## 8.8 Bitacora de auditoria

[ESPACIO PARA CAPTURA 08]

Instruccion:

1. Inicia sesion como Admin.
2. Entra a Bitacora.
3. Captura registros de acciones administrativas.

Evidencia esperada:

La bitacora debe mostrar fecha, usuario, accion y descripcion.

## 8.9 Prueba de restricciones SQL

[ESPACIO PARA CAPTURA 09]

Instruccion:

1. En SQL Server ejecuta una consulta a `sys.check_constraints`.
2. Captura constraints como `CK_materias_cupo_positivo`, `CK_inscripciones_estado_valido`, `CK_tickets_tipo_valido`, `CK_pagos_estado_valido`, etc.

Consulta sugerida:

```sql
SELECT name
FROM sys.check_constraints
WHERE parent_object_id IN (
    OBJECT_ID('materias'),
    OBJECT_ID('pagos'),
    OBJECT_ID('tickets_soporte'),
    OBJECT_ID('inscripciones'),
    OBJECT_ID('alumnos')
);
```

## 8.10 Prueba de usuarios de semestres altos

[ESPACIO PARA CAPTURA 10]

Instruccion:

1. Ejecuta `BD/agregar_alumnos_altos_semestres_demo.sql`.
2. Captura el resultado final de la consulta.
3. Entra al sistema con `AlumnoSis4`, `AlumnoCom4` o `AlumnoAdm4`.
4. Captura que cada uno ve materias de su carrera y semestre.

Evidencia esperada:

Esto demuestra que el filtro no depende de un solo usuario, sino de la carrera y semestre del perfil.

---

# 9. Evidencia de pruebas y control de calidad

Pruebas realizadas:

1. Login con usuario valido.
2. Validacion de menu por rol.
3. Alumno consultando solo su perfil.
4. Alumno viendo materias solo de su carrera.
5. Alumno viendo materias solo de su semestre.
6. Inscripcion con validacion de cupo.
7. Bloqueo de inscripcion duplicada.
8. Pago simulado con tarjeta valida.
9. Rechazo de tarjeta sin numero, titular, CVV o expiracion valida.
10. Generacion de comprobante.
11. Consulta de Mis pagos.
12. Creacion de ticket de soporte.
13. Cambio de estatus de ticket por administrador.
14. Registro de acciones en bitacora.
15. Validacion de CHECK constraints en SQL Server.

Errores encontrados y correcciones:

| Error o deficiencia | Correccion aplicada |
| --- | --- |
| Alumno/docente tenian dashboards casi vacios. | Se agregaron tarjetas, accesos rapidos y vistas por rol. |
| Faltaba flujo real de pagos para alumno. | Se implemento pago simulado, validacion de tarjeta, comprobante y Mis pagos. |
| No existia modulo visible de soporte. | Se agregaron tickets de soporte y seguimiento de estatus. |
| La baja existia solo como estado. | Se formalizo con motivo y fecha de baja. |
| Faltaban restricciones de datos. | Se agregaron CHECK constraints para estados, cupo, semestre, prioridad, tipo de ticket y pago. |
| Bitacora solo podia comprobarse por SQL. | Se agrego pantalla de Bitacora. |
| Materias podian confundirse entre carreras. | Se reforzo filtro por carrera y semestre en backend y frontend. |
| Faltaban materias/profesores para prueba sin inscripciones. | Se agrego script demo de materias y docentes asignados. |
| No habia usuarios de semestres altos para validar filtros. | Se agrego script demo con AlumnoSis4, AlumnoCom4 y AlumnoAdm4. |

---

# 10. Calidad total aplicada

El sistema mejora la calidad desde cuatro enfoques:

Prevencion:

- Validaciones antes de guardar inscripciones, pagos y tickets.
- Restricciones en base de datos para evitar valores invalidos.
- Permisos por rol para reducir acciones indebidas.

Deteccion:

- Mensajes de error comprensibles.
- Tickets de soporte para reportar problemas reales.
- Bitacora para detectar cambios administrativos.

Correccion:

- Cambio de estado de inscripciones.
- Baja formal con motivo y fecha.
- Administracion de pagos y tickets.

Trazabilidad:

- `logs_auditoria` registra acciones.
- Tickets conservan estatus y fecha de actualizacion.
- Pagos tienen referencia/comprobante.

---

# 11. Limitaciones conocidas

El sistema esta preparado para una entrega academica funcional, no como despliegue productivo final.

Limitaciones:

- El pago es simulado y no se conecta con una pasarela bancaria real.
- La base de datos actual no incluye una tabla formal de horarios y salones. Si una materia no tiene ese dato, la interfaz muestra "No registrado".
- La mitigacion ante alta demanda se basa en JWT, consultas parametrizadas, filtros por usuario y validaciones en backend/BD, pero no sustituye una prueba de carga profesional.
- Se recomienda agregar pruebas automatizadas si el proyecto continua.

---

# 12. Conclusion de calidad

El Sistema Administrativo Educativo corrige los puntos principales del caso original al pasar de un sistema con altas basicas y datos inconsistentes a una solucion con reglas de negocio, permisos, integridad de base de datos, pagos simulados, soporte y auditoria.

La mejora no se limita a la interfaz. Las validaciones se aplican en frontend, backend y SQL Server, lo que reduce el riesgo de datos incorrectos incluso si hay errores de usuario o alta demanda. Tambien se agregaron evidencias verificables: tabla de requerimientos, scripts SQL, diagrama de base de datos, capturas de modulos, comprobantes de pago, tickets y bitacora.

Con esto, el proyecto cumple el objetivo academico de demostrar aseguramiento de calidad en requerimientos, base de datos, arquitectura, experiencia de usuario y evidencia de funcionamiento.

---

# 13. Participacion de integrantes

[ESPACIO PARA PARTICIPACION]

Instruccion: escribe aqui los integrantes del equipo y que hizo cada quien. Ejemplo:

- Integrante 1: analisis del caso y tabla de requerimientos.
- Integrante 2: base de datos y scripts SQL.
- Integrante 3: backend y validaciones.
- Integrante 4: frontend y evidencias.
- Integrante 5: pruebas y documentacion.

---

# 14. Anexos

Usuarios demo:

| Usuario | Password | Rol | Uso |
| --- | --- | --- | --- |
| Admin | Admin123 | ADMINISTRADOR | CRUD, pagos, tickets, bitacora. |
| Alumno1 | Admin123 | ALUMNO | Inscripcion, pago, comprobante y mis pagos. |
| Docente1 | Admin123 | DOCENTE | Consulta academica. |
| AlumnoSis4 | Admin123 | ALUMNO | Prueba de Sistemas en semestre alto. |
| AlumnoCom4 | Admin123 | ALUMNO | Prueba de Comunicacion en semestre alto. |
| AlumnoAdm4 | Admin123 | ALUMNO | Prueba de Administracion en semestre alto. |

Comando backend:

```powershell
cd "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo"
$env:JWT_SECRET_KEY="SistemaAdministrativoEscolarJWT2026Super"
$env:DB_SERVER="localhost"
$env:DB_NAME="CalidadYPruebas_SE"
.\.venv\Scripts\python.exe backend\main.py
```

Comando frontend:

```powershell
cd "C:\Users\gabit\OneDrive\Documentos\cosas de la skul\Semestre 8\Calidad y Pruebas\Sistema Administrativo Educativo\frontend"
python -m http.server 8000
```
