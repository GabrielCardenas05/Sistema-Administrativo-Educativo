USE CalidadYPruebas_SE;
GO

-- Roles base
IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ADMINISTRADOR') INSERT INTO roles (nombre) VALUES ('ADMINISTRADOR');
IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ADMINISTRATIVO') INSERT INTO roles (nombre) VALUES ('ADMINISTRATIVO');
IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'DOCENTE') INSERT INTO roles (nombre) VALUES ('DOCENTE');
IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ALUMNO') INSERT INTO roles (nombre) VALUES ('ALUMNO');
GO

DECLARE @hash VARCHAR(255) = '$2b$12$7b0Let54bulcuk80cIQesewhdu3kkTHQqQrVH9EwhJ.pR3GdPENt.'; -- Admin123
DECLARE @rolAdmin INT = (SELECT id_rol FROM roles WHERE UPPER(nombre) = 'ADMINISTRADOR');
DECLARE @rolAdmvo INT = (SELECT id_rol FROM roles WHERE UPPER(nombre) = 'ADMINISTRATIVO');
DECLARE @rolDocente INT = (SELECT id_rol FROM roles WHERE UPPER(nombre) = 'DOCENTE');
DECLARE @rolAlumno INT = (SELECT id_rol FROM roles WHERE UPPER(nombre) = 'ALUMNO');

-- Usuarios demo
IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Admin')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Admin', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'ControlEscolar')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('ControlEscolar', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Docente1')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Docente1', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Docente2')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Docente2', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Alumno1')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Alumno1', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Alumno2')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Alumno2', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Alumno3')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Alumno3', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Alumno4')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Alumno4', @hash, 1, GETDATE(), GETDATE());

IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Alumno5')
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at) VALUES ('Alumno5', @hash, 1, GETDATE(), GETDATE());

-- Asignacion de roles
INSERT INTO Usuario_Rol (id_usuario, id_rol)
SELECT u.id_usuario, v.id_rol
FROM usuarios u
JOIN (VALUES
    ('Admin', @rolAdmin),
    ('ControlEscolar', @rolAdmvo),
    ('Docente1', @rolDocente),
    ('Docente2', @rolDocente),
    ('Alumno1', @rolAlumno),
    ('Alumno2', @rolAlumno),
    ('Alumno3', @rolAlumno),
    ('Alumno4', @rolAlumno),
    ('Alumno5', @rolAlumno)
) v(usuario, id_rol) ON u.usuario = v.usuario
WHERE NOT EXISTS (
    SELECT 1 FROM Usuario_Rol ur
    WHERE ur.id_usuario = u.id_usuario AND ur.id_rol = v.id_rol
);
GO

-- Catalogos
IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Ingenieria en Sistemas')
    INSERT INTO carreras (nombre, activa) VALUES ('Ingenieria en Sistemas', 1);

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Administracion')
    INSERT INTO carreras (nombre, activa) VALUES ('Administracion', 1);

IF NOT EXISTS (SELECT 1 FROM periodos WHERE nombre = '2026-1')
    INSERT INTO periodos (nombre, activo) VALUES ('2026-1', 1);
GO

DECLARE @sistemas INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Ingenieria en Sistemas');
DECLARE @adminCarrera INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Administracion');

-- Materias
IF NOT EXISTS (SELECT 1 FROM materias WHERE clave = 'SIS101')
    INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
    VALUES ('SIS101', 'Fundamentos de Programacion', @sistemas, 1, 30, 1);

IF NOT EXISTS (SELECT 1 FROM materias WHERE clave = 'MAT101')
    INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
    VALUES ('MAT101', 'Algebra Lineal', @sistemas, 1, 25, 1);

IF NOT EXISTS (SELECT 1 FROM materias WHERE clave = 'COM101')
    INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
    VALUES ('COM101', 'Comunicacion Oral y Escrita', @sistemas, 1, 20, 1);

IF NOT EXISTS (SELECT 1 FROM materias WHERE clave = 'ADM101')
    INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
    VALUES ('ADM101', 'Introduccion a la Administracion', @adminCarrera, 1, 25, 1);
GO

DECLARE @sistemas2 INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Ingenieria en Sistemas');
DECLARE @adminCarrera2 INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Administracion');

-- Docentes
IF NOT EXISTS (SELECT 1 FROM docentes WHERE id_usuario = (SELECT id_usuario FROM usuarios WHERE usuario = 'Docente1'))
    INSERT INTO docentes (id_usuario, nombre, especialidad)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Docente1'), 'Laura Martinez Ruiz', 'Programacion');

IF NOT EXISTS (SELECT 1 FROM docentes WHERE id_usuario = (SELECT id_usuario FROM usuarios WHERE usuario = 'Docente2'))
    INSERT INTO docentes (id_usuario, nombre, especialidad)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Docente2'), 'Carlos Hernandez Soto', 'Matematicas');
GO

DECLARE @sistemas3 INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Ingenieria en Sistemas');
DECLARE @adminCarrera3 INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Administracion');

-- Alumnos
IF NOT EXISTS (SELECT 1 FROM alumnos WHERE matricula = '2026001')
    INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Alumno1'), '2026001', 'Juan Perez Lopez', 'PELJ060101HDFRPN01', @sistemas3, 1, 'ACTIVO');

IF NOT EXISTS (SELECT 1 FROM alumnos WHERE matricula = '2026002')
    INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Alumno2'), '2026002', 'Maria Garcia Ramos', 'GARM060202MDFRMS02', @sistemas3, 1, 'ACTIVO');

IF NOT EXISTS (SELECT 1 FROM alumnos WHERE matricula = '2026003')
    INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Alumno3'), '2026003', 'Diego Sanchez Cruz', 'SACD060303HDFNRG03', @sistemas3, 1, 'ACTIVO');

IF NOT EXISTS (SELECT 1 FROM alumnos WHERE matricula = '2026004')
    INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Alumno4'), '2026004', 'Ana Torres Vega', 'TOVA060404MDFRNN04', @sistemas3, 1, 'ACTIVO');

IF NOT EXISTS (SELECT 1 FROM alumnos WHERE matricula = '2026005')
    INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
    VALUES ((SELECT id_usuario FROM usuarios WHERE usuario = 'Alumno5'), '2026005', 'Luis Morales Diaz', 'MODL060505HDFRZS05', @adminCarrera3, 1, 'ACTIVO');
GO

-- Inscripciones de ejemplo
DECLARE @periodo INT = (SELECT id_periodo FROM periodos WHERE nombre = '2026-1');

INSERT INTO inscripciones (id_alumno, id_materia, id_periodo, estado, fecha_inscripcion)
SELECT a.id_alumno, m.id_materia, @periodo, v.estado, GETDATE()
FROM (VALUES
    ('2026001', 'SIS101', 'ACTIVA'),
    ('2026001', 'MAT101', 'ACTIVA'),
    ('2026002', 'SIS101', 'PENDIENTE'),
    ('2026002', 'COM101', 'ACTIVA'),
    ('2026003', 'MAT101', 'ACTIVA'),
    ('2026003', 'COM101', 'BAJA'),
    ('2026004', 'SIS101', 'ACTIVA'),
    ('2026005', 'ADM101', 'ACTIVA')
) v(matricula, clave, estado)
JOIN alumnos a ON a.matricula = v.matricula
JOIN materias m ON m.clave = v.clave
WHERE NOT EXISTS (
    SELECT 1 FROM inscripciones i
    WHERE i.id_alumno = a.id_alumno
      AND i.id_materia = m.id_materia
      AND i.id_periodo = @periodo
);
GO

SELECT 'Usuarios demo creados. Password para todos: Admin123' AS Resultado;
SELECT usuario FROM usuarios WHERE usuario IN ('Admin','ControlEscolar','Docente1','Docente2','Alumno1','Alumno2','Alumno3','Alumno4','Alumno5');

-- Pagos de ejemplo para demostracion
INSERT INTO pagos (id_inscripcion, monto, estado, fecha_pago)
SELECT i.id_inscripcion, v.monto, v.estado, v.fecha_pago
FROM (VALUES
    ('2026001', 'SIS101', 1500.00, 'PAGADO', GETDATE()),
    ('2026001', 'MAT101', 1500.00, 'PENDIENTE', NULL),
    ('2026002', 'SIS101', 1500.00, 'PENDIENTE', NULL),
    ('2026004', 'SIS101', 1500.00, 'PAGADO', GETDATE())
) v(matricula, clave, monto, estado, fecha_pago)
JOIN alumnos a ON a.matricula = v.matricula
JOIN materias m ON m.clave = v.clave
JOIN inscripciones i ON i.id_alumno = a.id_alumno AND i.id_materia = m.id_materia
WHERE NOT EXISTS (
    SELECT 1 FROM pagos p
    WHERE p.id_inscripcion = i.id_inscripcion
);
GO

-- Ticket de ejemplo: pago no reflejado
IF NOT EXISTS (
    SELECT 1 FROM tickets_soporte
    WHERE tipo = 'PAGO_NO_REFLEJADO'
      AND titulo = 'Pago pendiente de validacion'
)
BEGIN
    INSERT INTO tickets_soporte (
        id_usuario, tipo, titulo, descripcion, estatus,
        prioridad, id_inscripcion, fecha_creacion, fecha_actualizacion
    )
    SELECT
        u.id_usuario,
        'PAGO_NO_REFLEJADO',
        'Pago pendiente de validacion',
        'El alumno reporta que realizo el pago, pero aparece como pendiente en el sistema.',
        'ABIERTO',
        'ALTA',
        i.id_inscripcion,
        GETDATE(),
        GETDATE()
    FROM usuarios u
    JOIN alumnos a ON a.id_usuario = u.id_usuario
    JOIN inscripciones i ON i.id_alumno = a.id_alumno
    JOIN materias m ON m.id_materia = i.id_materia
    WHERE u.usuario = 'Alumno1' AND m.clave = 'MAT101';
END
GO
GO
