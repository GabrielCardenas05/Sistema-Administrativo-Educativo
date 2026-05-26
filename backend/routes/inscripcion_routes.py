from flask import Blueprint, request
from repositories.inscripcion_repo import (
    get_all_inscripciones, get_inscripciones_by_alumno,
    create_inscripcion, update_estado_inscripcion, delete_inscripcion
)
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO

inscripciones_bp = Blueprint("inscripciones", __name__, url_prefix="/api/inscripciones")


@inscripciones_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def listar_inscripciones(current_user):
    id_periodo = request.args.get("id_periodo", type=int)
    inscripciones = get_all_inscripciones(id_periodo=id_periodo)
    return ok(data=[i.to_dict() for i in inscripciones])


@inscripciones_bp.route("/alumno/<int:id_alumno>", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO, "ALUMNO", "DOCENTE")
def inscripciones_de_alumno(current_user, id_alumno):
    inscripciones = get_inscripciones_by_alumno(id_alumno)
    return ok(data=[i.to_dict() for i in inscripciones])


@inscripciones_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def crear_inscripcion(current_user):
    data = request.get_json(silent=True) or {}
    for campo in ["id_alumno", "id_materia", "id_periodo"]:
        if data.get(campo) is None:
            return error(f"El campo '{campo}' es requerido")
    try:
        resultado = create_inscripcion(
            id_alumno=data["id_alumno"],
            id_materia=data["id_materia"],
            id_periodo=data["id_periodo"],
        )
        return created(data=resultado, message="Inscripción creada correctamente")
    except Exception as e:
        if "UNIQUE" in str(e):
            return error("El alumno ya está inscrito en esa materia en ese periodo", 409)
        return error(f"Error al crear inscripción: {str(e)}")


@inscripciones_bp.route("/<int:id_inscripcion>/estado", methods=["PATCH"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def cambiar_estado(current_user, id_inscripcion):
    data = request.get_json(silent=True) or {}
    estado = data.get("estado", "")
    if not estado:
        return error("El campo 'estado' es requerido")
    if not update_estado_inscripcion(id_inscripcion, estado):
        return error("Estado inválido o inscripción no encontrada")
    return ok(message="Estado actualizado correctamente")


@inscripciones_bp.route("/<int:id_inscripcion>", methods=["DELETE"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def eliminar_inscripcion(current_user, id_inscripcion):
    if not delete_inscripcion(id_inscripcion):
        return not_found("Inscripción no encontrada")
    return ok(message="Inscripción eliminada correctamente")
