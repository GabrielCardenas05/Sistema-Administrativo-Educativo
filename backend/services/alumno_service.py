from repositories.auth_repo import get_usuario_by_username
from repositories.rol_repo import get_roles_by_user_id

from utils.security import verify_password


def login(username, password):

    usuario = get_usuario_by_username(username)

    if not usuario:
        return {
            "success": False,
            "message": "Usuario no encontrado"
        }

    if not usuario.activo:
        return {
            "success": False,
            "message": "Usuario inactivo"
        }

    password_correcta = verify_password(
        password,
        usuario.password_hash
    )

    if not password_correcta:
        return {
            "success": False,
            "message": "Contraseña incorrecta"
        }

    roles_db = get_roles_by_user_id(usuario.id_usuario)

    roles = []

    for rol in roles_db:
        roles.append(rol.nombre)

    return {
        "success": True,
        "message": "Login exitoso",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "usuario": usuario.usuario,
            "roles": roles
        }
    }