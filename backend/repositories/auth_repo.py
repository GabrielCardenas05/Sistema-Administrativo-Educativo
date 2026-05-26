from repositories.usuario_repo import get_usuario_by_username, get_roles_by_user_id


def get_usuario_con_roles(username: str):
    """
    Devuelve (usuario_obj, roles_list) o (None, []) si no existe.
    """
    usuario = get_usuario_by_username(username)
    if not usuario:
        return None, []
    roles = get_roles_by_user_id(usuario.id_usuario)
    return usuario, roles
