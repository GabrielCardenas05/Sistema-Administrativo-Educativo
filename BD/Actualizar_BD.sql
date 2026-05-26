-- ============================================================
-- Script de actualización BD: CalidadYPruebas_SE
-- Aplica los cambios post-desarrollo:
--   1. Quitar id_rol de usuarios
--   2. Crear tabla Usuario_Rol (muchos-a-muchos)
--   3. Agregar timestamps a usuarios
--   4. UNIQUE id_usuario en alumnos y docentes
-- ============================================================

USE CalidadYPruebas_SE;
GO

-- ────────────────────────────────────────────────────────────
-- PASO 1: Eliminar FK de id_rol en usuarios (si existe)
-- ────────────────────────────────────────────────────────────
-- Busca el nombre de la FK generada automáticamente y la elimina
DECLARE @fk_name NVARCHAR(200);
SELECT @fk_name = name
FROM sys.foreign_keys
WHERE parent_object_id = OBJECT_ID('usuarios')
  AND name LIKE '%id_rol%';

IF @fk_name IS NOT NULL
BEGIN
    EXEC ('ALTER TABLE usuarios DROP CONSTRAINT ' + @fk_name);
    PRINT 'FK id_rol eliminada: ' + @fk_name;
END
ELSE
    PRINT 'FK id_rol no encontrada (ya fue eliminada o no existe).';
GO

-- ────────────────────────────────────────────────────────────
-- PASO 2: Eliminar columna id_rol de usuarios (si existe)
-- ────────────────────────────────────────────────────────────
IF EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'id_rol'
)
BEGIN
    ALTER TABLE usuarios DROP COLUMN id_rol;
    PRINT 'Columna id_rol eliminada de usuarios.';
END
ELSE
    PRINT 'Columna id_rol ya no existe en usuarios.';
GO

-- ────────────────────────────────────────────────────────────
-- PASO 3: Agregar timestamps a usuarios (si no existen)
-- ────────────────────────────────────────────────────────────
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'created_at'
)
BEGIN
    ALTER TABLE usuarios ADD created_at DATETIME DEFAULT GETDATE();
    PRINT 'Columna created_at agregada a usuarios.';
END

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'usuarios' AND COLUMN_NAME = 'updated_at'
)
BEGIN
    ALTER TABLE usuarios ADD updated_at DATETIME DEFAULT GETDATE();
    PRINT 'Columna updated_at agregada a usuarios.';
END
GO

-- ────────────────────────────────────────────────────────────
-- PASO 4: Crear tabla Usuario_Rol (si no existe)
-- ────────────────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Usuario_Rol')
BEGIN
    CREATE TABLE Usuario_Rol (
        id_usuario INT NOT NULL,
        id_rol     INT NOT NULL,
        PRIMARY KEY (id_usuario, id_rol),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
        FOREIGN KEY (id_rol)     REFERENCES roles(id_rol)
    );
    PRINT 'Tabla Usuario_Rol creada.';
END
ELSE
    PRINT 'Tabla Usuario_Rol ya existe.';
GO

-- ────────────────────────────────────────────────────────────
-- PASO 5: UNIQUE id_usuario en alumnos (si no existe)
-- ────────────────────────────────────────────────────────────
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('alumnos') AND name = 'UQ_alumnos_id_usuario'
)
BEGIN
    ALTER TABLE alumnos ADD CONSTRAINT UQ_alumnos_id_usuario UNIQUE (id_usuario);
    PRINT 'UNIQUE id_usuario agregado a alumnos.';
END
ELSE
    PRINT 'UNIQUE id_usuario en alumnos ya existe.';
GO

-- ────────────────────────────────────────────────────────────
-- PASO 6: UNIQUE id_usuario en docentes (si no existe)
-- ────────────────────────────────────────────────────────────
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('docentes') AND name = 'UQ_docentes_id_usuario'
)
BEGIN
    ALTER TABLE docentes ADD CONSTRAINT UQ_docentes_id_usuario UNIQUE (id_usuario);
    PRINT 'UNIQUE id_usuario agregado a docentes.';
END
ELSE
    PRINT 'UNIQUE id_usuario en docentes ya existe.';
GO

-- ────────────────────────────────────────────────────────────
-- PASO 7: Asegurar roles base en la tabla roles
-- ────────────────────────────────────────────────────────────
IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ADMINISTRADOR')
    INSERT INTO roles (nombre) VALUES ('ADMINISTRADOR');

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ADMINISTRATIVO')
    INSERT INTO roles (nombre) VALUES ('ADMINISTRATIVO');

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'DOCENTE')
    INSERT INTO roles (nombre) VALUES ('DOCENTE');

IF NOT EXISTS (SELECT 1 FROM roles WHERE UPPER(nombre) = 'ALUMNO')
    INSERT INTO roles (nombre) VALUES ('ALUMNO');

PRINT 'Roles base verificados/insertados.';
GO

-- PASO 8: Crear tabla de auditoria si no existe
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'logs_auditoria')
BEGIN
    CREATE TABLE logs_auditoria (
        id_log INT IDENTITY(1,1) PRIMARY KEY,
        id_usuario INT NOT NULL,
        accion VARCHAR(100) NOT NULL,
        descripcion VARCHAR(MAX),
        fecha DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
    );
    PRINT 'Tabla logs_auditoria creada.';
END
ELSE
    PRINT 'Tabla logs_auditoria ya existe.';
GO

-- PASO 9: Indice de apoyo para reglas de inscripcion
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('inscripciones') AND name = 'IX_inscripciones_materia_estado'
)
BEGIN
    CREATE INDEX IX_inscripciones_materia_estado
    ON inscripciones (id_materia, estado);
    PRINT 'Indice IX_inscripciones_materia_estado creado.';
END
GO

-- ────────────────────────────────────────────────────────────
-- Verificación final
-- ────────────────────────────────────────────────────────────
SELECT 'usuarios' AS tabla, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'usuarios'
UNION ALL
SELECT 'Usuario_Rol', COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Usuario_Rol'
ORDER BY tabla, COLUMN_NAME;

SELECT * FROM roles ORDER BY id_rol;
GO

PRINT '✅ Actualización completada correctamente.';
GO
