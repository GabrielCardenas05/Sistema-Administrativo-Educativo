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

-- PASO 10: Crear tabla de pagos si no existe
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'pagos')
BEGIN
    CREATE TABLE pagos (
        id_pago INT IDENTITY(1,1) PRIMARY KEY,
        id_inscripcion INT NOT NULL,
        monto DECIMAL(10,2) NOT NULL,
        estado VARCHAR(20) DEFAULT 'PENDIENTE',
        fecha_pago DATETIME,
        FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
    );
    PRINT 'Tabla pagos creada.';
END
ELSE
    PRINT 'Tabla pagos ya existe.';
GO

-- PASO 11: Indice de apoyo para pagos
IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('pagos') AND name = 'IX_pagos_inscripcion'
)
BEGIN
    CREATE INDEX IX_pagos_inscripcion
    ON pagos (id_inscripcion, estado);
    PRINT 'Indice IX_pagos_inscripcion creado.';
END
GO

-- PASO 12: Crear tabla de tickets de soporte si no existe
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'tickets_soporte')
BEGIN
    CREATE TABLE tickets_soporte (
        id_ticket INT IDENTITY(1,1) PRIMARY KEY,
        id_usuario INT NOT NULL,
        tipo VARCHAR(50) NOT NULL,
        titulo VARCHAR(150) NOT NULL,
        descripcion VARCHAR(MAX) NOT NULL,
        estatus VARCHAR(20) DEFAULT 'ABIERTO',
        prioridad VARCHAR(20) DEFAULT 'MEDIA',
        id_inscripcion INT NULL,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_actualizacion DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
        FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
    );
    PRINT 'Tabla tickets_soporte creada.';
END
ELSE
    PRINT 'Tabla tickets_soporte ya existe.';
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('tickets_soporte') AND name = 'IX_tickets_soporte_usuario_estatus'
)
BEGIN
    CREATE INDEX IX_tickets_soporte_usuario_estatus
    ON tickets_soporte (id_usuario, estatus);
    PRINT 'Indice IX_tickets_soporte_usuario_estatus creado.';
END
GO

IF NOT EXISTS (
    SELECT 1 FROM sys.indexes
    WHERE object_id = OBJECT_ID('tickets_soporte') AND name = 'IX_tickets_soporte_estatus'
)
BEGIN
    CREATE INDEX IX_tickets_soporte_estatus
    ON tickets_soporte (estatus, fecha_creacion);
    PRINT 'Indice IX_tickets_soporte_estatus creado.';
END
GO

-- PASO 13: Columnas para flujo formal de bajas
IF OBJECT_ID('inscripciones', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'inscripciones' AND COLUMN_NAME = 'motivo_baja'
    )
    BEGIN
        ALTER TABLE inscripciones ADD motivo_baja VARCHAR(255) NULL;
        PRINT 'Columna motivo_baja agregada a inscripciones.';
    END

    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'inscripciones' AND COLUMN_NAME = 'fecha_baja'
    )
    BEGIN
        ALTER TABLE inscripciones ADD fecha_baja DATETIME NULL;
        PRINT 'Columna fecha_baja agregada a inscripciones.';
    END
END
GO

-- PASO 13.1: Columnas de comprobante y metodo de pago simulado
IF OBJECT_ID('pagos', 'U') IS NOT NULL
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'pagos' AND COLUMN_NAME = 'metodo_pago'
    )
    BEGIN
        ALTER TABLE pagos ADD metodo_pago VARCHAR(30) NULL;
        PRINT 'Columna metodo_pago agregada a pagos.';
    END

    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'pagos' AND COLUMN_NAME = 'titular'
    )
    BEGIN
        ALTER TABLE pagos ADD titular VARCHAR(100) NULL;
        PRINT 'Columna titular agregada a pagos.';
    END

    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'pagos' AND COLUMN_NAME = 'tarjeta_ultimos4'
    )
    BEGIN
        ALTER TABLE pagos ADD tarjeta_ultimos4 CHAR(4) NULL;
        PRINT 'Columna tarjeta_ultimos4 agregada a pagos.';
    END

    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'pagos' AND COLUMN_NAME = 'referencia'
    )
    BEGIN
        ALTER TABLE pagos ADD referencia VARCHAR(50) NULL;
        PRINT 'Columna referencia agregada a pagos.';
    END

    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'pagos' AND COLUMN_NAME = 'concepto'
    )
    BEGIN
        ALTER TABLE pagos ADD concepto VARCHAR(150) NULL;
        PRINT 'Columna concepto agregada a pagos.';
    END

    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'pagos' AND COLUMN_NAME = 'fecha_creacion'
    )
    BEGIN
        ALTER TABLE pagos ADD fecha_creacion DATETIME NULL;
        PRINT 'Columna fecha_creacion agregada a pagos.';
    END
END
GO

-- PASO 14: Normalizar datos existentes antes de agregar CHECK constraints
IF OBJECT_ID('usuarios', 'U') IS NOT NULL
BEGIN
    UPDATE usuarios
    SET activo = 1
    WHERE activo IS NULL;
END
GO

IF OBJECT_ID('carreras', 'U') IS NOT NULL
BEGIN
    UPDATE carreras
    SET activa = 1
    WHERE activa IS NULL;
END
GO

IF OBJECT_ID('alumnos', 'U') IS NOT NULL
BEGIN
    UPDATE alumnos
    SET semestre = 1
    WHERE semestre IS NULL OR semestre NOT BETWEEN 1 AND 10;

    UPDATE alumnos
    SET estatus = 'ACTIVO'
    WHERE estatus IS NULL OR UPPER(estatus) NOT IN ('ACTIVO', 'INACTIVO', 'EGRESADO', 'BAJA');
END
GO

IF OBJECT_ID('materias', 'U') IS NOT NULL
BEGIN
    UPDATE materias
    SET semestre = 1
    WHERE semestre IS NULL OR semestre NOT BETWEEN 1 AND 10;

    UPDATE materias
    SET cupo = 1
    WHERE cupo IS NULL OR cupo <= 0;

    UPDATE materias
    SET activa = 1
    WHERE activa IS NULL;
END
GO

IF OBJECT_ID('periodos', 'U') IS NOT NULL
BEGIN
    UPDATE periodos
    SET activo = 0
    WHERE activo IS NULL;
END
GO

IF OBJECT_ID('inscripciones', 'U') IS NOT NULL
BEGIN
    UPDATE inscripciones
    SET estado = 'PENDIENTE'
    WHERE estado IS NULL OR UPPER(estado) NOT IN ('PENDIENTE', 'ACTIVA', 'BAJA', 'FINALIZADA');

    UPDATE inscripciones
    SET motivo_baja = COALESCE(NULLIF(LTRIM(RTRIM(motivo_baja)), ''), 'Baja migrada desde estado existente'),
        fecha_baja = COALESCE(fecha_baja, fecha_inscripcion, GETDATE())
    WHERE UPPER(estado) = 'BAJA'
      AND (motivo_baja IS NULL OR LTRIM(RTRIM(motivo_baja)) = '' OR fecha_baja IS NULL);
END
GO

IF OBJECT_ID('pagos', 'U') IS NOT NULL
BEGIN
    UPDATE pagos
    SET monto = 1.00
    WHERE monto IS NULL OR monto <= 0;

    UPDATE pagos
    SET estado = 'PENDIENTE'
    WHERE estado IS NULL OR UPPER(estado) NOT IN ('PENDIENTE', 'PAGADO', 'RECHAZADO');

    UPDATE pagos
    SET metodo_pago = 'TARJETA'
    WHERE metodo_pago IS NULL OR UPPER(metodo_pago) NOT IN ('TARJETA');

    UPDATE pagos
    SET referencia = CONCAT('PAY-', RIGHT('000000' + CAST(id_pago AS VARCHAR(6)), 6))
    WHERE referencia IS NULL OR LTRIM(RTRIM(referencia)) = '';

    UPDATE pagos
    SET concepto = 'Pago de inscripcion'
    WHERE concepto IS NULL OR LTRIM(RTRIM(concepto)) = '';

    UPDATE pagos
    SET fecha_creacion = COALESCE(fecha_pago, GETDATE())
    WHERE fecha_creacion IS NULL;

    UPDATE pagos
    SET tarjeta_ultimos4 = NULL
    WHERE tarjeta_ultimos4 IS NOT NULL AND tarjeta_ultimos4 NOT LIKE '[0-9][0-9][0-9][0-9]';
END
GO

IF OBJECT_ID('tickets_soporte', 'U') IS NOT NULL
BEGIN
    UPDATE tickets_soporte
    SET tipo = 'OTRO'
    WHERE tipo IS NULL OR UPPER(tipo) NOT IN ('MATERIA_INCORRECTA', 'PAGO_NO_REFLEJADO', 'ERROR_SISTEMA', 'OTRO');

    UPDATE tickets_soporte
    SET estatus = 'ABIERTO'
    WHERE estatus IS NULL OR UPPER(estatus) NOT IN ('ABIERTO', 'EN_REVISION', 'RESUELTO', 'CERRADO');

    UPDATE tickets_soporte
    SET prioridad = 'MEDIA'
    WHERE prioridad IS NULL OR UPPER(prioridad) NOT IN ('BAJA', 'MEDIA', 'ALTA');
END
GO

-- PASO 15: CHECK constraints de integridad de datos
IF OBJECT_ID('usuarios', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('usuarios') AND name = 'CK_usuarios_activo'
)
BEGIN
    ALTER TABLE usuarios WITH CHECK ADD CONSTRAINT CK_usuarios_activo CHECK (activo IS NOT NULL AND activo IN (0, 1));
    PRINT 'CHECK CK_usuarios_activo agregado.';
END
GO

IF OBJECT_ID('carreras', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('carreras') AND name = 'CK_carreras_activa'
)
BEGIN
    ALTER TABLE carreras WITH CHECK ADD CONSTRAINT CK_carreras_activa CHECK (activa IS NOT NULL AND activa IN (0, 1));
    PRINT 'CHECK CK_carreras_activa agregado.';
END
GO

IF OBJECT_ID('alumnos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('alumnos') AND name = 'CK_alumnos_semestre_valido'
)
BEGIN
    ALTER TABLE alumnos WITH CHECK ADD CONSTRAINT CK_alumnos_semestre_valido CHECK (semestre BETWEEN 1 AND 10);
    PRINT 'CHECK CK_alumnos_semestre_valido agregado.';
END
GO

IF OBJECT_ID('alumnos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('alumnos') AND name = 'CK_alumnos_estatus_valido'
)
BEGIN
    ALTER TABLE alumnos WITH CHECK ADD CONSTRAINT CK_alumnos_estatus_valido CHECK (estatus IS NOT NULL AND UPPER(estatus) IN ('ACTIVO', 'INACTIVO', 'EGRESADO', 'BAJA'));
    PRINT 'CHECK CK_alumnos_estatus_valido agregado.';
END
GO

IF OBJECT_ID('materias', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('materias') AND name = 'CK_materias_semestre_valido'
)
BEGIN
    ALTER TABLE materias WITH CHECK ADD CONSTRAINT CK_materias_semestre_valido CHECK (semestre BETWEEN 1 AND 10);
    PRINT 'CHECK CK_materias_semestre_valido agregado.';
END
GO

IF OBJECT_ID('materias', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('materias') AND name = 'CK_materias_cupo_positivo'
)
BEGIN
    ALTER TABLE materias WITH CHECK ADD CONSTRAINT CK_materias_cupo_positivo CHECK (cupo > 0);
    PRINT 'CHECK CK_materias_cupo_positivo agregado.';
END
GO

IF OBJECT_ID('materias', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('materias') AND name = 'CK_materias_activa'
)
BEGIN
    ALTER TABLE materias WITH CHECK ADD CONSTRAINT CK_materias_activa CHECK (activa IS NOT NULL AND activa IN (0, 1));
    PRINT 'CHECK CK_materias_activa agregado.';
END
GO

IF OBJECT_ID('periodos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('periodos') AND name = 'CK_periodos_activo'
)
BEGIN
    ALTER TABLE periodos WITH CHECK ADD CONSTRAINT CK_periodos_activo CHECK (activo IS NOT NULL AND activo IN (0, 1));
    PRINT 'CHECK CK_periodos_activo agregado.';
END
GO

IF OBJECT_ID('inscripciones', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('inscripciones') AND name = 'CK_inscripciones_estado_valido'
)
BEGIN
    ALTER TABLE inscripciones WITH CHECK ADD CONSTRAINT CK_inscripciones_estado_valido CHECK (estado IS NOT NULL AND UPPER(estado) IN ('PENDIENTE', 'ACTIVA', 'BAJA', 'FINALIZADA'));
    PRINT 'CHECK CK_inscripciones_estado_valido agregado.';
END
GO

IF OBJECT_ID('inscripciones', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('inscripciones') AND name = 'CK_inscripciones_baja_formal'
)
BEGIN
    ALTER TABLE inscripciones WITH CHECK ADD CONSTRAINT CK_inscripciones_baja_formal CHECK (
        UPPER(estado) <> 'BAJA'
        OR (motivo_baja IS NOT NULL AND LTRIM(RTRIM(motivo_baja)) <> '' AND fecha_baja IS NOT NULL)
    );
    PRINT 'CHECK CK_inscripciones_baja_formal agregado.';
END
GO

IF OBJECT_ID('pagos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('pagos') AND name = 'CK_pagos_monto_positivo'
)
BEGIN
    ALTER TABLE pagos WITH CHECK ADD CONSTRAINT CK_pagos_monto_positivo CHECK (monto > 0);
    PRINT 'CHECK CK_pagos_monto_positivo agregado.';
END
GO

IF OBJECT_ID('pagos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('pagos') AND name = 'CK_pagos_estado_valido'
)
BEGIN
    ALTER TABLE pagos WITH CHECK ADD CONSTRAINT CK_pagos_estado_valido CHECK (estado IS NOT NULL AND UPPER(estado) IN ('PENDIENTE', 'PAGADO', 'RECHAZADO'));
    PRINT 'CHECK CK_pagos_estado_valido agregado.';
END
GO

IF OBJECT_ID('pagos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('pagos') AND name = 'CK_pagos_metodo_valido'
)
BEGIN
    ALTER TABLE pagos WITH CHECK ADD CONSTRAINT CK_pagos_metodo_valido CHECK (metodo_pago IS NOT NULL AND UPPER(metodo_pago) IN ('TARJETA'));
    PRINT 'CHECK CK_pagos_metodo_valido agregado.';
END
GO

IF OBJECT_ID('pagos', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('pagos') AND name = 'CK_pagos_tarjeta_ultimos4'
)
BEGIN
    ALTER TABLE pagos WITH CHECK ADD CONSTRAINT CK_pagos_tarjeta_ultimos4 CHECK (
        tarjeta_ultimos4 IS NULL OR tarjeta_ultimos4 LIKE '[0-9][0-9][0-9][0-9]'
    );
    PRINT 'CHECK CK_pagos_tarjeta_ultimos4 agregado.';
END
GO

IF OBJECT_ID('tickets_soporte', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('tickets_soporte') AND name = 'CK_tickets_tipo_valido'
)
BEGIN
    ALTER TABLE tickets_soporte WITH CHECK ADD CONSTRAINT CK_tickets_tipo_valido CHECK (tipo IS NOT NULL AND UPPER(tipo) IN ('MATERIA_INCORRECTA', 'PAGO_NO_REFLEJADO', 'ERROR_SISTEMA', 'OTRO'));
    PRINT 'CHECK CK_tickets_tipo_valido agregado.';
END
GO

IF OBJECT_ID('tickets_soporte', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('tickets_soporte') AND name = 'CK_tickets_estatus_valido'
)
BEGIN
    ALTER TABLE tickets_soporte WITH CHECK ADD CONSTRAINT CK_tickets_estatus_valido CHECK (estatus IS NOT NULL AND UPPER(estatus) IN ('ABIERTO', 'EN_REVISION', 'RESUELTO', 'CERRADO'));
    PRINT 'CHECK CK_tickets_estatus_valido agregado.';
END
GO

IF OBJECT_ID('tickets_soporte', 'U') IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM sys.check_constraints
    WHERE parent_object_id = OBJECT_ID('tickets_soporte') AND name = 'CK_tickets_prioridad_valida'
)
BEGIN
    ALTER TABLE tickets_soporte WITH CHECK ADD CONSTRAINT CK_tickets_prioridad_valida CHECK (prioridad IS NOT NULL AND UPPER(prioridad) IN ('BAJA', 'MEDIA', 'ALTA'));
    PRINT 'CHECK CK_tickets_prioridad_valida agregado.';
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
