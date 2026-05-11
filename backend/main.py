from controllers.auth_controller import login_controller


response = login_controller(
    "admin",
    "admin123"
)

print(response)