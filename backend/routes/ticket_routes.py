from flask import Blueprint, request
from repositories.ticket_repo import (
    get_all_tickets, get_tickets_by_usuario, create_ticket,
    update_ticket_status, inscripcion_belongs_to_usuario
)
from repositories.audit_repo import log_audit
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO

tickets_bp = Blueprint("tickets", __name__, url_prefix="/api/tickets")


def _has_role(current_user, *roles):
    user_roles = [r.upper() for r in current_user.get("roles", [])]
    return any(r.upper() in user_roles for r in roles)


@tickets_bp.route("/", methods=["GET"])
@require_auth
def listar_tickets(current_user):
    if _has_role(current_user, ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO):
        tickets = get_all_tickets()
    else:
        tickets = get_tickets_by_usuario(current_user["id_usuario"])
    return ok(data=tickets)


@tickets_bp.route("/", methods=["POST"])
@require_auth
def crear_ticket(current_user):
    data = request.get_json(silent=True) or {}
    tipo = (data.get("tipo") or "").strip().upper()
    titulo = (data.get("titulo") or "").strip()
    descripcion = (data.get("descripcion") or "").strip()
    prioridad = (data.get("prioridad") or "MEDIA").strip().upper()
    id_inscripcion = data.get("id_inscripcion")

    if not tipo or not titulo or not descripcion:
        return error("tipo, titulo y descripcion son requeridos")
    if tipo not in {"MATERIA_INCORRECTA", "PAGO_NO_REFLEJADO", "ERROR_SISTEMA", "OTRO"}:
        return error("Tipo de ticket inválido")
    if prioridad not in {"BAJA", "MEDIA", "ALTA"}:
        return error("Prioridad inválida")

    if id_inscripcion is not None:
        try:
            id_inscripcion = int(id_inscripcion)
        except (TypeError, ValueError):
            return error("id_inscripcion inválido")

        if _has_role(current_user, "ALUMNO") and not inscripcion_belongs_to_usuario(
            id_inscripcion, current_user["id_usuario"]
        ):
            return error("No puedes reportar una inscripción que no te pertenece", 403)

    resultado = create_ticket(
        id_usuario=current_user["id_usuario"],
        tipo=tipo,
        titulo=titulo,
        descripcion=descripcion,
        prioridad=prioridad,
        id_inscripcion=id_inscripcion,
    )
    log_audit(current_user["id_usuario"], "CREAR_TICKET", f"id_ticket={resultado.get('id_ticket')}")
    return created(data=resultado, message="Ticket generado correctamente")


@tickets_bp.route("/<int:id_ticket>/estatus", methods=["PATCH"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def actualizar_estatus_ticket(current_user, id_ticket):
    data = request.get_json(silent=True) or {}
    estatus = (data.get("estatus") or "").strip().upper()
    if estatus not in {"ABIERTO", "EN_REVISION", "RESUELTO", "CERRADO"}:
        return error("Estatus inválido")
    if not update_ticket_status(id_ticket, estatus):
        return not_found("Ticket no encontrado")
    log_audit(current_user["id_usuario"], "ACTUALIZAR_TICKET", f"id_ticket={id_ticket}, estatus={estatus}")
    return ok(message="Ticket actualizado correctamente")
