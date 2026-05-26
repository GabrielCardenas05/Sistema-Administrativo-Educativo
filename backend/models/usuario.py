class Usuario:
    def __init__(self, id_usuario, usuario, password_hash, activo, created_at=None, updated_at=None):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.password_hash = password_hash
        self.activo = bool(activo)
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "usuario": self.usuario,
            "activo": self.activo,
        }
