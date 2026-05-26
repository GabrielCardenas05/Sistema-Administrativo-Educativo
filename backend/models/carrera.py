class Carrera:
    def __init__(self, id_carrera, nombre, activa=True):
        self.id_carrera = id_carrera
        self.nombre = nombre
        self.activa = bool(activa)

    def to_dict(self):
        return {
            "id_carrera": self.id_carrera,
            "nombre": self.nombre,
            "activa": self.activa,
        }
