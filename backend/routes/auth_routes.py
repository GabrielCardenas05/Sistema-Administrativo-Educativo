from flask import Blueprint, request
from services.auth_service import login
from utils.responses import ok, error

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json(silent=True) or {}
    username = data.get("usuario", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return error("usuario y password son requeridos")

    result = login(username, password)

    if result["success"]:
        return ok(
            data={"token": result["token"], "usuario": result["usuario"]},
            message=result["message"]
        )
    return error(result["message"], 401)


@auth_bp.route("/me", methods=["GET"])
def me():
    """Verifica el token y devuelve info del usuario autenticado."""
    from utils.auth_decorators import require_auth
    from flask import g
    # Verificación manual para este endpoint
    from utils.security import verify_token
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return error("Token requerido", 401)
    decoded = verify_token(auth_header.split(" ", 1)[1])
    if not decoded:
        return error("Token inválido o expirado", 401)
    return ok(data={
        "id_usuario": decoded["id_usuario"],
        "usuario": decoded["usuario"],
        "roles": decoded["roles"],
    })
