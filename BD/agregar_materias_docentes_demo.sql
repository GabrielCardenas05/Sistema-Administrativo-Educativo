USE CalidadYPruebas_SE;
GO

IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'materia_docente')
BEGIN
    CREATE TABLE materia_docente (
        id_materia INT NOT NULL,
        id_docente INT NOT NULL,
        PRIMARY KEY (id_materia, id_docente),
        FOREIGN KEY (id_materia) REFERENCES materias(id_materia),
        FOREIGN KEY (id_docente) REFERENCES docentes(id_docente)
    );
END
GO

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Ingenieria en Sistemas')
    INSERT INTO carreras (nombre, activa) VALUES ('Ingenieria en Sistemas', 1);

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Comunicacion')
    INSERT INTO carreras (nombre, activa) VALUES ('Comunicacion', 1);

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Administracion')
    INSERT INTO carreras (nombre, activa) VALUES ('Administracion', 1);
GO

DECLARE @hash VARCHAR(255) = '$2b$12$7b0Let54bulcuk80cIQesewhdu3kkTHQqQrVH9EwhJ.pR3GdPENt.'; -- Admin123
DECLARE @rolDocente INT = (SELECT id_rol FROM roles WHERE UPPER(nombre) = 'DOCENTE');

INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at)
SELECT v.usuario, @hash, 1, GETDATE(), GETDATE()
FROM (VALUES
    ('DocSistemas'),
    ('DocComunicacion'),
    ('DocAdministracion')
) v(usuario)
WHERE NOT EXISTS (SELECT 1 FROM usuarios u WHERE u.usuario = v.usuario);

INSERT INTO Usuario_Rol (id_usuario, id_rol)
SELECT u.id_usuario, @rolDocente
FROM usuarios u
WHERE u.usuario IN ('DocSistemas', 'DocComunicacion', 'DocAdministracion')
  AND NOT EXISTS (
      SELECT 1 FROM Usuario_Rol ur
      WHERE ur.id_usuario = u.id_usuario AND ur.id_rol = @rolDocente
  );

INSERT INTO docentes (id_usuario, nombre, especialidad)
SELECT u.id_usuario, v.nombre, v.especialidad
FROM (VALUES
    ('DocSistemas', 'Roberto Salinas Torres', 'Ingenieria en Sistemas'),
    ('DocComunicacion', 'Patricia Medina Rios', 'Comunicacion'),
    ('DocAdministracion', 'Elena Navarro Cruz', 'Administracion')
) v(usuario, nombre, especialidad)
JOIN usuarios u ON u.usuario = v.usuario
WHERE NOT EXISTS (SELECT 1 FROM docentes d WHERE d.id_usuario = u.id_usuario);
GO

DECLARE @sistemas INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Ingenieria en Sistemas');
DECLARE @comunicacion INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Comunicacion');
DECLARE @administracion INT = (SELECT id_carrera FROM carreras WHERE nombre = 'Administracion');

INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
SELECT v.clave, v.nombre, v.id_carrera, v.semestre, v.cupo, 1
FROM (VALUES
    ('SIS201', 'Estructuras de Datos', @sistemas, 2, 30),
    ('SIS301', 'Bases de Datos', @sistemas, 3, 28),
    ('SIS401', 'Calidad de Software', @sistemas, 4, 25),
    ('COM201', 'Redaccion Periodistica', @comunicacion, 2, 30),
    ('COM301', 'Teoria de la Comunicacion', @comunicacion, 3, 28),
    ('COM401', 'Produccion Audiovisual', @comunicacion, 4, 24),
    ('ADM201', 'Contabilidad Administrativa', @administracion, 2, 30),
    ('ADM301', 'Mercadotecnia', @administracion, 3, 28),
    ('ADM401', 'Gestion de Proyectos', @administracion, 4, 24)
) v(clave, nombre, id_carrera, semestre, cupo)
WHERE NOT EXISTS (SELECT 1 FROM materias m WHERE m.clave = v.clave);

INSERT INTO materia_docente (id_materia, id_docente)
SELECT m.id_materia, d.id_docente
FROM (VALUES
    ('SIS201', 'DocSistemas'),
    ('SIS301', 'DocSistemas'),
    ('SIS401', 'DocSistemas'),
    ('COM201', 'DocComunicacion'),
    ('COM301', 'DocComunicacion'),
    ('COM401', 'DocComunicacion'),
    ('ADM201', 'DocAdministracion'),
    ('ADM301', 'DocAdministracion'),
    ('ADM401', 'DocAdministracion')
) v(clave, usuario_docente)
JOIN materias m ON m.clave = v.clave
JOIN usuarios u ON u.usuario = v.usuario_docente
JOIN docentes d ON d.id_usuario = u.id_usuario
WHERE NOT EXISTS (
    SELECT 1 FROM materia_docente md
    WHERE md.id_materia = m.id_materia AND md.id_docente = d.id_docente
);
GO

SELECT
    c.nombre AS carrera,
    m.clave,
    m.nombre AS materia,
    m.semestre,
    d.nombre AS docente
FROM materias m
JOIN carreras c ON c.id_carrera = m.id_carrera
LEFT JOIN materia_docente md ON md.id_materia = m.id_materia
LEFT JOIN docentes d ON d.id_docente = md.id_docente
WHERE m.clave IN (
    'SIS201','SIS301','SIS401',
    'COM201','COM301','COM401',
    'ADM201','ADM301','ADM401'
)
ORDER BY c.nombre, m.semestre, m.clave;
GO
