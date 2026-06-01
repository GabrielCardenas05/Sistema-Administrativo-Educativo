from flask import Blueprint, request
from repositories.pago_repo import get_all_pagos, create_pago, update_pago
from repositories.audit_repo import log_audit
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO

pagos_bp = Blueprint("pagos", __name__, url_prefix="/api/pagos")


@pagos_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def listar_pagos(current_user):
    return ok(data=get_all_pagos())


@pagos_bp.route("/", methods=["POST"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def crear_pago(current_user):
    data = request.get_json(silent=True) or {}
    if data.get("id_inscripcion") is None or data.get("monto") is None:
        return error("id_inscripcion y monto son requeridos")

    try:
        monto = float(data["monto"])
    except (TypeError, ValueError):
        return error("Monto inválido")
    if monto <= 0:
        return error("El monto debe ser mayor a cero")

    estado = (data.get("estado") or "PENDIENTE").upper()
    if estado not in {"PENDIENTE", "PAGADO", "RECHAZADO"}:
        return error("Estado de pago inválido")

    try:
        resultado = create_pago(
            id_inscripcion=int(data["id_inscripcion"]),
            monto=monto,
            estado=estado,
            fecha_pago=data.get("fecha_pago"),
        )
        log_audit(current_user["id_usuario"], "CREAR_PAGO", f"id_pago={resultado.get('id_pago')}")
        return created(data=resultado, message="Pago registrado correctamente")
    except Exception as e:
        return error(f"Error al registrar pago: {str(e)}")


@pagos_bp.route("/<int:id_pago>", methods=["PUT"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def actualizar_pago(current_user, id_pago):
    data = request.get_json(silent=True) or {}
    if "monto" in data:
        try:
            data["monto"] = float(data["monto"])
        except (TypeError, ValueError):
            return error("Monto inválido")
        if data["monto"] <= 0:
            return error("El monto debe ser mayor a cero")
    if "estado" in data:
        data["estado"] = str(data["estado"]).upper()
        if data["estado"] not in {"PENDIENTE", "PAGADO", "RECHAZADO"}:
            return error("Estado de pago inválido")

    try:
        if not update_pago(id_pago, data):
            return not_found("Pago no encontrado o sin cambios")
        log_audit(current_user["id_usuario"], "ACTUALIZAR_PAGO", f"id_pago={id_pago}")
        return ok(message="Pago actualizado correctamente")
    except Exception as e:
        return error(f"Error al actualizar pago: {str(e)}")
