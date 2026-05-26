from flask import jsonify


def ok(data=None, message="OK", status=200):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def created(data=None, message="Creado correctamente"):
    return ok(data, message, 201)


def error(message="Error", status=400):
    return jsonify({"success": False, "message": message}), status


def not_found(message="No encontrado"):
    return error(message, 404)


def server_error(message="Error interno del servidor"):
    return error(message, 500)
