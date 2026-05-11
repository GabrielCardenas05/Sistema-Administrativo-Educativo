class Usuario:

    def __init__(
        self,
        id_usuario,
        usuario,
        password_hash,
        activo=True
    ):

        self.id_usuario = id_usuario
        self.usuario = usuario
        self.password_hash = password_hash
        self.activo = activo