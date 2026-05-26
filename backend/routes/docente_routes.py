from flask import Blueprint, request
from repositories.docente_repo import (
    get_all_docentes, get_docente_by_id,
    create_docente, update_docente, delete_docente
)
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO
from repositories.audit_repo import log_audit

docentes_bp = Blueprint("docentes", __name__, url_prefix="/api/docentes")


@docentes_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def listar_docentes(current_user):
    docentes = get_all_docentes()
    return ok(data=[d.to_dict() for d in docentes])


@docentes_bp.route("/<int:id_docente>", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def obtener_docente(current_user, id_docente):
    docente = get_docente_by_id(id_docente)
    if not docente:
        return not_found("Docente no encontrado")
    return ok(data=docente.to_dict())


@docentes_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def crear_docente(current_user):
    data = request.get_json(silent=True) or {}
    for campo in ["id_usuario", "nombre"]:
        if not data.get(campo):
            return error(f"El campo '{campo}' es requerido")
    try:
        resultado = create_docente(
            id_usuario=data["id_usuario"],
            nombre=data["nombre"],
            especialidad=data.get("especialidad"),
        )
        log_audit(current_user["id_usuario"], "CREAR_DOCENTE", f"id_docente={resultado.get('id_docente')}")
        return created(data=resultado, message="Docente creado correctamente")
    except Exception as e:
        if "UNIQUE" in str(e):
            return error("Este usuario ya está registrado como docente", 409)
        return error(f"Error al crear docente: {str(e)}")


@docentes_bp.route("/<int:id_docente>", methods=["PUT"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def actualizar_docente(current_user, id_docente):
    data = request.get_json(silent=True) or {}
    if not update_docente(id_docente, data):
        return error("No se pudo actualizar (no existe o sin cambios)")
    log_audit(current_user["id_usuario"], "ACTUALIZAR_DOCENTE", f"id_docente={id_docente}")
    return ok(message="Docente actualizado correctamente")


@docentes_bp.route("/<int:id_docente>", methods=["DELETE"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def eliminar_docente(current_user, id_docente):
    if not delete_docente(id_docente):
        return not_found("Docente no encontrado")
    log_audit(current_user["id_usuario"], "ELIMINAR_DOCENTE", f"id_docente={id_docente}")
    return ok(message="Docente eliminado correctamente")
