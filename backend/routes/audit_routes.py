from flask import Blueprint, request
from repositories.audit_repo import get_audit_logs
from utils.auth_decorators import require_auth, require_role
from utils.responses import ok
from utils.constants import ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO

auditoria_bp = Blueprint("auditoria", __name__, url_prefix="/api/auditoria")


@auditoria_bp.route("/", methods=["GET"])
@require_auth
@require_role(ROL_ADMINISTRADOR, ROL_ADMINISTRATIVO)
def listar_bitacora(current_user):
    limit = request.args.get("limit", default=200, type=int)
    limit = max(1, min(limit, 500))
    return ok(data=get_audit_logs(limit=limit))
