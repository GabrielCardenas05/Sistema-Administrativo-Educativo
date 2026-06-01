USE CalidadYPruebas_SE;
GO

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ALUMNO')
    INSERT INTO roles (nombre) VALUES ('ALUMNO');
GO

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Ingenieria en Sistemas')
    INSERT INTO carreras (nombre, activa) VALUES ('Ingenieria en Sistemas', 1);

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Comunicacion')
    INSERT INTO carreras (nombre, activa) VALUES ('Comunicacion', 1);

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Administracion')
    INSERT INTO carreras (nombre, activa) VALUES ('Administracion', 1);
GO

DECLARE @hash VARCHAR(255) = '$2b$12$7b0Let54bulcuk80cIQesewhdu3kkTHQqQrVH9EwhJ.pR3GdPENt.'; -- Admin123
DECLARE @rolAlumno INT = (SELECT id_rol FROM roles WHERE UPPER(nombre) = 'ALUMNO');

INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at)
SELECT v.usuario, @hash, 1, GETDATE(), GETDATE()
FROM (VALUES
    ('AlumnoSis2'),
    ('AlumnoSis3'),
    ('AlumnoSis4'),
    ('AlumnoCom2'),
    ('AlumnoCom3'),
    ('AlumnoCom4'),
    ('AlumnoAdm2'),
    ('AlumnoAdm3'),
    ('AlumnoAdm4')
) v(usuario)
WHERE NOT EXISTS (SELECT 1 FROM usuarios u WHERE u.usuario = v.usuario);

INSERT INTO Usuario_Rol (id_usuario, id_rol)
SELECT u.id_usuario, @rolAlumno
FROM usuarios u
WHERE u.usuario IN (
    'AlumnoSis2','AlumnoSis3','AlumnoSis4',
    'AlumnoCom2','AlumnoCom3','AlumnoCom4',
    'AlumnoAdm2','AlumnoAdm3','AlumnoAdm4'
)
AND NOT EXISTS (
    SELECT 1 FROM Usuario_Rol ur
    WHERE ur.id_usuario = u.id_usuario AND ur.id_rol = @rolAlumno
);
GO

DECLARE @sistemas INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Ingenieria en Sistemas');
DECLARE @comunicacion INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Comunicacion');
DECLARE @administracion INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Administracion');

INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
SELECT u.id_usuario, v.matricula, v.nombre, v.curp, v.id_carrera, v.semestre, 'ACTIVO'
FROM (VALUES
    ('AlumnoSis2', '2026202', 'Sofia Rios Sistemas', 'RISS060202MDFSSL02', @sistemas, 2),
    ('AlumnoSis3', '2026303', 'Mateo Cruz Sistemas', 'CUSM060303HDFSTR03', @sistemas, 3),
    ('AlumnoSis4', '2026404', 'Valeria Leon Sistemas', 'LEVV060404MDFSNL04', @sistemas, 4),
    ('AlumnoCom2', '2027202', 'Daniela Mora Comunicacion', 'MODD060202MDFCMN02', @comunicacion, 2),
    ('AlumnoCom3', '2027303', 'Hector Luna Comunicacion', 'LUHH060303HDFCMR03', @comunicacion, 3),
    ('AlumnoCom4', '2027404', 'Camila Soto Comunicacion', 'SOCC060404MDFCMS04', @comunicacion, 4),
    ('AlumnoAdm2', '2028202', 'Emilio Vargas Administracion', 'VAEE060202HDFADM02', @administracion, 2),
    ('AlumnoAdm3', '2028303', 'Paula Neri Administracion', 'NEPP060303MDFADM03', @administracion, 3),
    ('AlumnoAdm4', '2028404', 'Oscar Ponce Administracion', 'POOO060404HDFADM04', @administracion, 4)
) v(usuario, matricula, nombre, curp, id_carrera, semestre)
JOIN usuarios u ON u.usuario = v.usuario
WHERE NOT EXISTS (SELECT 1 FROM alumnos a WHERE a.matricula = v.matricula);
GO

SELECT
    u.usuario,
    'Admin123' AS password_demo,
    a.matricula,
    a.nombre AS alumno,
    c.nombre AS carrera,
    a.semestre,
    COUNT(m.id_materia) AS materias_visibles_esperadas
FROM alumnos a
JOIN usuarios u ON u.id_usuario = a.id_usuario
JOIN carreras c ON c.id_carrera = a.id_carrera
LEFT JOIN materias m ON m.id_carrera = a.id_carrera
    AND m.semestre = a.semestre
    AND m.activa = 1
WHERE u.usuario IN (
    'AlumnoSis2','AlumnoSis3','AlumnoSis4',
    'AlumnoCom2','AlumnoCom3','AlumnoCom4',
    'AlumnoAdm2','AlumnoAdm3','AlumnoAdm4'
)
GROUP BY u.usuario, a.matricula, a.nombre, c.nombre, a.semestre
ORDER BY c.nombre, a.semestre, u.usuario;
GO
