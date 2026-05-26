from functools import wraps
from flask import request, jsonify
from utils.security import verify_token


def require_auth(f):
    """
    Valida que el request lleve un JWT válido en el header Authorization.
    Inyecta `current_user` (dict con id_usuario, usuario, roles) al endpoint.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "message": "Token requerido"}), 401

        token = auth_header.split(" ", 1)[1]
        decoded = verify_token(token)
        if not decoded:
            return jsonify({"success": False, "message": "Token inválido o expirado"}), 401

        return f(decoded, *args, **kwargs)
    return wrapper


def require_role(*roles):
    """
    Restringe el acceso a uno o más roles.
    Uso: @require_role("ADMINISTRADOR")  o  @require_role("ADMINISTRADOR", "ADMINISTRATIVO")
    """
    def decorator(f):
        @wraps(f)
        def wrapper(current_user, *args, **kwargs):
            user_roles = [r.upper() for r in current_user.get("roles", [])]
            required = [r.upper() for r in roles]
            if not any(r in user_roles for r in required):
                return jsonify({"success": False, "message": "Acceso denegado"}), 403
            return f(current_user, *args, **kwargs)
        return wrapper
    return decorator
