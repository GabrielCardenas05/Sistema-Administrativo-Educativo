from controllers.auth_controller import login_controller

from utils.auth_decorators import (
    require_auth,
    require_role
)


response = login_controller(
    "admin",
    "admin123"
)

token = response["token"]


@require_auth
@require_role("DOCENTE")
def admin_panel(decoded):

    return {
        "success": True,
        "message": f"Bienvenido {decoded['usuario']}"
    }


result = admin_panel(token)

print(result)