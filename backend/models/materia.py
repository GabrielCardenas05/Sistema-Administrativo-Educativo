class Materia:
    def __init__(self, id_materia, clave, nombre, id_carrera, semestre, cupo, activa=True):
        self.id_materia = id_materia
        self.clave = clave
        self.nombre = nombre
        self.id_carrera = id_carrera
        self.semestre = semestre
        self.cupo = cupo
        self.activa = bool(activa)

    def to_dict(self):
        return {
            "id_materia": self.id_materia,
            "clave": self.clave,
            "nombre": self.nombre,
            "id_carrera": self.id_carrera,
            "semestre": self.semestre,
            "cupo": self.cupo,
            "activa": self.activa,
        }
