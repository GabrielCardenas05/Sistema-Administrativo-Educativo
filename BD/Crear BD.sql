CREATE TABLE roles (
    id_rol INT PRIMARY KEY IDENTITY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY IDENTITY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    activo BIT DEFAULT 1,

    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);
CREATE TABLE carreras (
    id_carrera INT PRIMARY KEY IDENTITY,
    nombre VARCHAR(100) NOT NULL,
    activa BIT DEFAULT 1
);
CREATE TABLE alumnos (
    id_alumno INT PRIMARY KEY IDENTITY,
    id_usuario INT NOT NULL,
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
    id_docente INT PRIMARY KEY IDENTITY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
CREATE TABLE administrativos (
    id_admin INT PRIMARY KEY IDENTITY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    puesto VARCHAR(50),

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
CREATE TABLE materias (
    id_materia INT PRIMARY KEY IDENTITY,
    clave VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    id_carrera INT NOT NULL,
    semestre INT NOT NULL,
    cupo INT NOT NULL,
    activa BIT DEFAULT 1,

    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);
CREATE TABLE periodos (
    id_periodo INT PRIMARY KEY IDENTITY,
    nombre VARCHAR(50) NOT NULL,
    activo BIT DEFAULT 0
);
CREATE TABLE inscripciones (
    id_inscripcion INT PRIMARY KEY IDENTITY,
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
CREATE TABLE pagos (
    id_pago INT PRIMARY KEY IDENTITY,
    id_inscripcion INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_pago DATETIME,

    FOREIGN KEY (id_inscripcion) REFERENCES inscripciones(id_inscripcion)
);
CREATE TABLE logs_auditoria (
    id_log INT PRIMARY KEY IDENTITY,
    id_usuario INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
