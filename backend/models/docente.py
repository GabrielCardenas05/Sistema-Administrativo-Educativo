class Docente:
    def __init__(self, id_docente, id_usuario, nombre, especialidad=None):
        self.id_docente = id_docente
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.especialidad = especialidad

    def to_dict(self):
        return {
            "id_docente": self.id_docente,
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "especialidad": self.especialidad,
        }
