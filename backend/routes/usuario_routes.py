from flask import Blueprint, request
from repositories.usuario_repo import (
    get_all_usuarios, get_usuario_by_id,
    create_usuario, update_usuario, delete_usuario
)
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR
from repositories.audit_repo import log_audit

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")


@usuarios_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def listar_usuarios(current_user):
    usuarios = get_all_usuarios()
    return ok(data=[u.to_dict() for u in usuarios])


@usuarios_bp.route("/<int:id_usuario>", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def obtener_usuario(current_user, id_usuario):
    usuario = get_usuario_by_id(id_usuario)
    if not usuario:
        return not_found("Usuario no encontrado")
    return ok(data=usuario.to_dict())


@usuarios_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def crear_usuario(current_user):
    data = request.get_json(silent=True) or {}
    campos = ["usuario", "password", "roles"]
    for campo in campos:
        if not data.get(campo):
            return error(f"El campo '{campo}' es requerido")

    try:
        resultado = create_usuario(
            usuario=data["usuario"],
            password=data["password"],
            roles=data["roles"],
        )
        log_audit(current_user["id_usuario"], "CREAR_USUARIO", f"id_usuario={resultado.get('id_usuario')}")
        return created(data=resultado, message="Usuario creado correctamente")
    except Exception as e:
        if "UNIQUE" in str(e):
            return error("El nombre de usuario ya existe", 409)
        if isinstance(e, ValueError):
            return error(str(e), 400)
        return error(f"Error al crear usuario: {str(e)}")


@usuarios_bp.route("/<int:id_usuario>", methods=["PUT"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def actualizar_usuario(current_user, id_usuario):
    data = request.get_json(silent=True) or {}
    if not update_usuario(id_usuario, data):
        return error("No se pudo actualizar el usuario (no existe o sin cambios)")
    log_audit(current_user["id_usuario"], "ACTUALIZAR_USUARIO", f"id_usuario={id_usuario}")
    return ok(message="Usuario actualizado correctamente")


@usuarios_bp.route("/<int:id_usuario>", methods=["DELETE"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def eliminar_usuario(current_user, id_usuario):
    if not delete_usuario(id_usuario):
        return not_found("Usuario no encontrado")
    log_audit(current_user["id_usuario"], "ELIMINAR_USUARIO", f"id_usuario={id_usuario}")
    return ok(message="Usuario eliminado correctamente")
