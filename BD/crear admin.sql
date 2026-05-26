USE CalidadYPruebas_SE;
GO

-- Roles base
IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ADMINISTRADOR')
    INSERT INTO roles (nombre) VALUES ('ADMINISTRADOR');

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ADMINISTRATIVO')
    INSERT INTO roles (nombre) VALUES ('ADMINISTRATIVO');

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'DOCENTE')
    INSERT INTO roles (nombre) VALUES ('DOCENTE');

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ALUMNO')
    INSERT INTO roles (nombre) VALUES ('ALUMNO');
GO

-- Usuario admin: Admin / Admin123
IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario = 'Admin')
BEGIN
    INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at)
    VALUES (
        'Admin',
        '$2b$12$7b0Let54bulcuk80cIQesewhdu3kkTHQqQrVH9EwhJ.pR3GdPENt.',
        1,
        GETDATE(),
        GETDATE()
    );
END
GO

-- Asignar rol ADMINISTRADOR
DECLARE @id_usuario INT;
DECLARE @id_rol INT;

SELECT @id_usuario = id_usuario FROM usuarios WHERE usuario = 'Admin';
SELECT @id_rol = id_rol FROM roles WHERE UPPER(nombre) = 'ADMINISTRADOR';

IF NOT EXISTS (
    SELECT 1 FROM Usuario_Rol
    WHERE id_usuario = @id_usuario AND id_rol = @id_rol
)
BEGIN
    INSERT INTO Usuario_Rol (id_usuario, id_rol)
    VALUES (@id_usuario, @id_rol);
END
GO

-- Datos mínimos para probar el sistema
IF NOT EXISTS (SELECT 1 FROM periodos WHERE nombre = '2026-1')
    INSERT INTO periodos (nombre, activo) VALUES ('2026-1', 1);

IF NOT EXISTS (SELECT 1 FROM carreras WHERE nombre = 'Ingeniería en Sistemas')
    INSERT INTO carreras (nombre, activa) VALUES ('Ingeniería en Sistemas', 1);

IF NOT EXISTS (SELECT 1 FROM materias WHERE clave = 'SIS101')
BEGIN
    INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
    SELECT 'SIS101', 'Fundamentos de Programación', id_carrera, 1, 30, 1
    FROM carreras
    WHERE nombre = 'Ingeniería en Sistemas';
END
GO