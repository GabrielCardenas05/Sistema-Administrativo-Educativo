from functools import wraps

from utils.security import verify_token


def require_auth(func):

    @wraps(func)
    def wrapper(token, *args, **kwargs):

        decoded = verify_token(token)

        if not decoded:
            return {
                "success": False,
                "message": "Token invalido o expirado"
            }

        return func(decoded, *args, **kwargs)

    return wrapper


def require_role(required_role):

    def decorator(func):

        @wraps(func)
        def wrapper(decoded, *args, **kwargs):

            user_roles = decoded.get("roles", [])

            if required_role not in user_roles:

                return {
                    "success": False,
                    "message": "Acceso denegado"
                }

            return func(decoded, *args, **kwargs)

        return wrapper

    return decorator