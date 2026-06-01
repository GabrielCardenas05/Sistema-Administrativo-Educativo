import re
from datetime import date

from flask import Blueprint, request
from repositories.pago_repo import (
    get_all_pagos, get_pagos_by_usuario, create_pago,
    create_pago_for_student, update_pago
)
from repositories.audit_repo import log_audit
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok, created, error, not_found
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO, ROL_ALUMNO

pagos_bp = Blueprint("pagos", __name__, url_prefix="/api/pagos")
MONTO_INSCRIPCION = 1500.00


def _luhn_ok(number: str) -> bool:
    total = 0
    reverse_digits = number[::-1]
    for index, char in enumerate(reverse_digits):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def _validate_expiration(value: str) -> bool:
    value = (value or "").strip()
    match = re.fullmatch(r"(\d{4})-(\d{2})", value)
    if match:
        year, month = int(match.group(1)), int(match.group(2))
    else:
        match = re.fullmatch(r"(\d{2})/(\d{2}|\d{4})", value)
        if not match:
            return False
        month = int(match.group(1))
        year = int(match.group(2))
        if year < 100:
            year += 2000
    if month < 1 or month > 12:
        return False
    today = date.today()
    return (year, month) >= (today.year, today.month)


def _validate_card_payload(data):
    titular = (data.get("titular") or "").strip()
    tarjeta = re.sub(r"\D", "", data.get("tarjeta_numero") or "")
    cvv = (data.get("cvv") or "").strip()
    expiracion = (data.get("expiracion") or "").strip()

    if len(titular) < 4 or not re.search(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]", titular):
        return None, "El titular de la tarjeta es inválido"
    if not re.fullmatch(r"\d{13,19}", tarjeta) or not _luhn_ok(tarjeta):
        return None, "El número de tarjeta no cumple con el formato requerido"
    if not re.fullmatch(r"\d{3,4}", cvv):
        return None, "El CVV debe tener 3 o 4 dígitos"
    if not _validate_expiration(expiracion):
        return None, "La fecha de expiración es inválida o ya venció"
    return {"titular": titular, "tarjeta_ultimos4": tarjeta[-4:]}, None


@pagos_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def listar_pagos(current_user):
    return ok(data=get_all_pagos())


@pagos_bp.route("/mis-pagos", methods=["GET"])
@require_auth
@require_role(ROL_ALUMNO)
def mis_pagos(current_user):
    return ok(data=get_pagos_by_usuario(current_user["id_usuario"]))


@pagos_bp.route("/pagar-inscripcion", methods=["POST"])
@require_auth
@require_role(ROL_ALUMNO)
def pagar_inscripcion(current_user):
    data = request.get_json(silent=True) or {}
    if data.get("id_materia") is None:
        return error("id_materia es requerido")

    tarjeta, mensaje = _validate_card_payload(data)
    if mensaje:
        return error(mensaje)

    try:
        resultado = create_pago_for_student(
            id_usuario=current_user["id_usuario"],
            id_materia=int(data["id_materia"]),
            titular=tarjeta["titular"],
            tarjeta_ultimos4=tarjeta["tarjeta_ultimos4"],
            monto=MONTO_INSCRIPCION,
        )
        log_audit(
            current_user["id_usuario"],
            "PAGO_ALUMNO",
            f"id_pago={resultado.get('id_pago')}, referencia={resultado.get('referencia')}",
        )
        return created(data=resultado, message="Inscripción y pago registrados correctamente")
    except ValueError as e:
        return error(str(e))
    except Exception as e:
        return error(f"Error al registrar pago: {str(e)}")


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
    if data.get("metodo_pago") and str(data["metodo_pago"]).upper() != "TARJETA":
        return error("Método de pago inválido")
    if data.get("tarjeta_ultimos4") and not re.fullmatch(r"\d{4}", str(data["tarjeta_ultimos4"])):
        return error("Los últimos 4 dígitos de tarjeta son inválidos")

    try:
        resultado = create_pago(
            id_inscripcion=int(data["id_inscripcion"]),
            monto=monto,
            estado=estado,
            fecha_pago=data.get("fecha_pago"),
            metodo_pago=data.get("metodo_pago") or "TARJETA",
            titular=data.get("titular"),
            tarjeta_ultimos4=data.get("tarjeta_ultimos4"),
            referencia=data.get("referencia"),
            concepto=data.get("concepto"),
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
    if "metodo_pago" in data:
        data["metodo_pago"] = str(data["metodo_pago"]).upper()
        if data["metodo_pago"] != "TARJETA":
            return error("Método de pago inválido")
    if "tarjeta_ultimos4" in data and data["tarjeta_ultimos4"]:
        if not re.fullmatch(r"\d{4}", str(data["tarjeta_ultimos4"])):
            return error("Los últimos 4 dígitos de tarjeta son inválidos")

    try:
        if not update_pago(id_pago, data):
            return not_found("Pago no encontrado o sin cambios")
        log_audit(current_user["id_usuario"], "ACTUALIZAR_PAGO", f"id_pago={id_pago}")
        return ok(message="Pago actualizado correctamente")
    except Exception as e:
        return error(f"Error al actualizar pago: {str(e)}")
