from flask import Blueprint, request
from repositories.materia_repo import (
    get_all_materias, get_materia_by_id,
    create_materia, update_materia, delete_materia
)
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO
from repositories.audit_repo import log_audit

materias_bp = Blueprint("materias", __name__, url_prefix="/api/materias")


@materias_bp.route("/", methods=["GET"])
@require_auth
def listar_materias(current_user):
    id_carrera = request.args.get("id_carrera", type=int)
    semestre = request.args.get("semestre", type=int)
    materias = get_all_materias(id_carrera=id_carrera, semestre=semestre)
    return ok(data=[m.to_dict() for m in materias])


@materias_bp.route("/<int:id_materia>", methods=["GET"])
@require_auth
def obtener_materia(current_user, id_materia):
    materia = get_materia_by_id(id_materia)
    if not materia:
        return not_found("Materia no encontrada")
    return ok(data=materia.to_dict())


@materias_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def crear_materia(current_user):
    data = request.get_json(silent=True) or {}
    requeridos = ["clave", "nombre", "id_carrera", "semestre", "cupo"]
    for campo in requeridos:
        if data.get(campo) is None:
            return error(f"El campo '{campo}' es requerido")
    try:
        resultado = create_materia(
            clave=data["clave"],
            nombre=data["nombre"],
            id_carrera=data["id_carrera"],
            semestre=data["semestre"],
            cupo=data["cupo"],
        )
        log_audit(current_user["id_usuario"], "CREAR_MATERIA", f"id_materia={resultado.get('id_materia')}")
        return created(data=resultado, message="Materia creada correctamente")
    except Exception as e:
        if "UNIQUE" in str(e):
            return error("La clave de materia ya existe", 409)
        return error(f"Error al crear materia: {str(e)}")


@materias_bp.route("/<int:id_materia>", methods=["PUT"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def actualizar_materia(current_user, id_materia):
    data = request.get_json(silent=True) or {}
    if not update_materia(id_materia, data):
        return error("No se pudo actualizar (no existe o sin cambios)")
    log_audit(current_user["id_usuario"], "ACTUALIZAR_MATERIA", f"id_materia={id_materia}")
    return ok(message="Materia actualizada correctamente")


@materias_bp.route("/<int:id_materia>", methods=["DELETE"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def eliminar_materia(current_user, id_materia):
    if not delete_materia(id_materia):
        return not_found("Materia no encontrada")
    log_audit(current_user["id_usuario"], "ELIMINAR_MATERIA", f"id_materia={id_materia}")
    return ok(message="Materia eliminada correctamente")
