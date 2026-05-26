from repositories.auth_repo import get_usuario_con_roles
from utils.security import verify_password, generate_token


def login(username: str, password: str) -> dict:
    usuario, roles = get_usuario_con_roles(username)

    if not usuario:
        return {"success": False, "message": "Usuario no encontrado"}

    if not usuario.activo:
        return {"success": False, "message": "Usuario inactivo"}

    if not verify_password(password, usuario.password_hash):
        return {"success": False, "message": "Contraseña incorrecta"}

    user_data = {
        "id_usuario": usuario.id_usuario,
        "usuario": usuario.usuario,
        "roles": roles,
    }

    token = generate_token(user_data)

    return {
        "success": True,
        "message": "Login exitoso",
        "token": token,
        "usuario": user_data,
    }
