class Inscripcion:
    def __init__(self, id_inscripcion, id_alumno, id_materia, id_periodo,
                 estado="PENDIENTE", fecha_inscripcion=None):
        self.id_inscripcion = id_inscripcion
        self.id_alumno = id_alumno
        self.id_materia = id_materia
        self.id_periodo = id_periodo
        self.estado = estado
        self.fecha_inscripcion = fecha_inscripcion

    def to_dict(self):
        return {
            "id_inscripcion": self.id_inscripcion,
            "id_alumno": self.id_alumno,
            "id_materia": self.id_materia,
            "id_periodo": self.id_periodo,
            "estado": self.estado,
            "fecha_inscripcion": str(self.fecha_inscripcion) if self.fecha_inscripcion else None,
        }
