CREATE DATABASE CalidadYPruebas_SE;
GO

USE CalidadYPruebas_SE;
GO

CREATE TABLE roles (
    id_rol INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    activo BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

CREATE TABLE Usuario_Rol (
    id_usuario INT NOT NULL,
    id_rol INT NOT NULL,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

CREATE TABLE carreras (
    id_carrera INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    activa BIT DEFAULT 1
);

CREATE TABLE alumnos (
    id_alumno INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    curp VARCHAR(18) NOT NULL UNIQUE,
    id_carrera INT NOT NULL,
    semestre INT NOT NULL,
    estatus VARCHAR(20) DEFAULT 'ACTIVO',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

CREATE TABLE docentes (
    id_docente INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE administrativos (
    id_admin INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    puesto VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE materias (
    id_materia INT IDENTITY(1,1) PRIMARY KEY,
    clave VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    id_carrera INT NOT NULL,
    semestre INT NOT NULL,
    cupo INT NOT NULL,
    activa BIT DEFAULT 1,
    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

CREATE TABLE periodos (
    id_periodo INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    activo BIT DEFAULT 0
);

CREATE TABLE inscripciones (
    id_inscripcion INT IDENTITY(1,1) PRIMARY KEY,
    id_alumno INT NOT NULL,
    id_materia INT NOT NULL,
    id_periodo INT NOT NULL,
    estado VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_inscripcion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno),
    FOREIGN KEY (id_materia) REFERENCES materias(id_materia),
    FOREIGN KEY (id_periodo) REFERENCES periodos(id_periodo),
    UNIQUE (id_alumno, id_materia, id_periodo)
);

CREATE INDEX IX_inscripciones_materia_estado
ON inscripciones (id_materia, estado);

CREATE TABLE pagos (
    id_pago INT IDENTITY(1,1) PRIMARY KEY,
    id_inscripcion INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_pago DATETIME,
    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
);

CREATE INDEX IX_pagos_inscripcion
ON pagos (id_inscripcion, estado);

CREATE TABLE logs_auditoria (
    id_log INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    descripcion VARCHAR(MAX),
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

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

CREATE INDEX IX_tickets_soporte_usuario_estatus
ON tickets_soporte (id_usuario, estatus);

CREATE INDEX IX_tickets_soporte_estatus
ON tickets_soporte (estatus, fecha_creacion);

INSERT INTO roles (nombre)
VALUES ('ADMINISTRADOR'), ('ADMINISTRATIVO'), ('DOCENTE'), ('ALUMNO');
GO
