class Inscripcion:
    def __init__(self, id_inscripcion, id_alumno, id_materia, id_periodo,
                 estado="PENDIENTE", fecha_inscripcion=None, id_pago=None,
                 monto_pago=None, estado_pago=None, fecha_pago=None):
        self.id_inscripcion = id_inscripcion
        self.id_alumno = id_alumno
        self.id_materia = id_materia
        self.id_periodo = id_periodo
        self.estado = estado
        self.fecha_inscripcion = fecha_inscripcion
        self.id_pago = id_pago
        self.monto_pago = monto_pago
        self.estado_pago = estado_pago
        self.fecha_pago = fecha_pago

    def to_dict(self):
        return {
            "id_inscripcion": self.id_inscripcion,
            "id_alumno": self.id_alumno,
            "id_materia": self.id_materia,
            "id_periodo": self.id_periodo,
            "estado": self.estado,
            "fecha_inscripcion": str(self.fecha_inscripcion) if self.fecha_inscripcion else None,
            "id_pago": self.id_pago,
            "monto_pago": float(self.monto_pago) if self.monto_pago is not None else None,
            "estado_pago": self.estado_pago,
            "fecha_pago": str(self.fecha_pago) if self.fecha_pago else None,
        }
