from flask import Blueprint, request
from repositories.carrera_repo import (
    get_all_carreras, get_carrera_by_id,
    create_carrera, update_carrera, delete_carrera
)
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO

carreras_bp = Blueprint("carreras", __name__, url_prefix="/api/carreras")


@carreras_bp.route("/", methods=["GET"])
@require_auth
def listar_carreras(current_user):
    solo_activas = request.args.get("activas", "false").lower() == "true"
    carreras = get_all_carreras(solo_activas=solo_activas)
    return ok(data=[c.to_dict() for c in carreras])


@carreras_bp.route("/<int:id_carrera>", methods=["GET"])
@require_auth
def obtener_carrera(current_user, id_carrera):
    carrera = get_carrera_by_id(id_carrera)
    if not carrera:
        return not_found("Carrera no encontrada")
    return ok(data=carrera.to_dict())


@carreras_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def crear_carrera(current_user):
    data = request.get_json(silent=True) or {}
    if not data.get("nombre"):
        return error("El campo 'nombre' es requerido")
    try:
        resultado = create_carrera(nombre=data["nombre"])
        return created(data=resultado, message="Carrera creada correctamente")
    except Exception as e:
        return error(f"Error al crear carrera: {str(e)}")


@carreras_bp.route("/<int:id_carrera>", methods=["PUT"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def actualizar_carrera(current_user, id_carrera):
    data = request.get_json(silent=True) or {}
    if not update_carrera(id_carrera, data):
        return error("No se pudo actualizar (no existe o sin cambios)")
    return ok(message="Carrera actualizada correctamente")


@carreras_bp.route("/<int:id_carrera>", methods=["DELETE"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def eliminar_carrera(current_user, id_carrera):
    if not delete_carrera(id_carrera):
        return not_found("Carrera no encontrada")
    return ok(message="Carrera eliminada correctamente")
