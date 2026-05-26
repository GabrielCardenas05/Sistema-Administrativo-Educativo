from flask import Blueprint, request
from repositories.alumno_repo import (
    get_all_alumnos, get_alumno_by_id,
    get_alumno_by_usuario_id, create_alumno, update_alumno, delete_alumno
)
from repositories.audit_repo import log_audit
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO, ROL_DOCENTE

alumnos_bp = Blueprint("alumnos", __name__, url_prefix="/api/alumnos")


@alumnos_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO, ROL_DOCENTE)
def listar_alumnos(current_user):
    alumnos = get_all_alumnos()
    return ok(data=[a.to_dict() for a in alumnos])


@alumnos_bp.route("/<int:id_alumno>", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO, ROL_DOCENTE)
def obtener_alumno(current_user, id_alumno):
    alumno = get_alumno_by_id(id_alumno)
    if not alumno:
        return not_found("Alumno no encontrado")
    return ok(data=alumno.to_dict())


@alumnos_bp.route("/me", methods=["GET"])
@require_auth
@require_role("ALUMNO")
def mi_perfil(current_user):
    """Un alumno puede ver su propio perfil."""
    alumno = get_alumno_by_usuario_id(current_user["id_usuario"])
    if not alumno:
        return not_found("Perfil de alumno no encontrado")
    return ok(data=alumno.to_dict())


@alumnos_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def crear_alumno(current_user):
    data = request.get_json(silent=True) or {}
    requeridos = ["id_usuario", "matricula", "nombre", "curp", "id_carrera", "semestre"]
    for campo in requeridos:
        if data.get(campo) is None:
            return error(f"El campo '{campo}' es requerido")

    try:
        resultado = create_alumno(
            id_usuario=data["id_usuario"],
            matricula=data["matricula"],
            nombre=data["nombre"],
            curp=data["curp"],
            id_carrera=data["id_carrera"],
            semestre=data["semestre"],
        )
        log_audit(current_user["id_usuario"], "CREAR_ALUMNO", f"id_alumno={resultado.get('id_alumno')}")
        return created(data=resultado, message="Alumno creado correctamente")
    except Exception as e:
        if "UNIQUE" in str(e):
            return error("Matrícula o CURP ya registrada", 409)
        return error(f"Error al crear alumno: {str(e)}")


@alumnos_bp.route("/<int:id_alumno>", methods=["PUT"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def actualizar_alumno(current_user, id_alumno):
    data = request.get_json(silent=True) or {}
    if not update_alumno(id_alumno, data):
        return error("No se pudo actualizar (no existe o sin cambios)")
    log_audit(current_user["id_usuario"], "ACTUALIZAR_ALUMNO", f"id_alumno={id_alumno}")
    return ok(message="Alumno actualizado correctamente")


@alumnos_bp.route("/<int:id_alumno>", methods=["DELETE"])
@require_auth
@require_role(ROL_ADMINISTRADOR)
def eliminar_alumno(current_user, id_alumno):
    if not delete_alumno(id_alumno):
        return not_found("Alumno no encontrado")
    log_audit(current_user["id_usuario"], "ELIMINAR_ALUMNO", f"id_alumno={id_alumno}")
    return ok(message="Alumno eliminado correctamente")
