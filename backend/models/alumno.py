class Alumno:
    def __init__(self, id_alumno, id_usuario, matricula, nombre, curp,
                 id_carrera, semestre, estatus="ACTIVO"):
        self.id_alumno = id_alumno
        self.id_usuario = id_usuario
        self.matricula = matricula
        self.nombre = nombre
        self.curp = curp
        self.id_carrera = id_carrera
        self.semestre = semestre
        self.estatus = estatus

    def to_dict(self):
        return {
            "id_alumno": self.id_alumno,
            "id_usuario": self.id_usuario,
            "matricula": self.matricula,
            "nombre": self.nombre,
            "curp": self.curp,
            "id_carrera": self.id_carrera,
            "semestre": self.semestre,
            "estatus": self.estatus,
        }
