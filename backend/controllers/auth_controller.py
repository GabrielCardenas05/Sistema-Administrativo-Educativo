from services.auth_service import login


def login_controller(username, password):

    response = login(username, password)

    return response