import sys
import os

# Asegura que el backend/ sea el directorio de imports
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.usuario_routes import usuarios_bp
from routes.alumno_routes import alumnos_bp
from routes.docente_routes import docentes_bp
from routes.carrera_routes import carreras_bp
from routes.materia_routes import materias_bp
from routes.inscripcion_routes import inscripciones_bp
from routes.ticket_routes import tickets_bp
from routes.pago_routes import pagos_bp
from routes.audit_routes import auditoria_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Registrar Blueprints ───────────────────────────────────────────────────────
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(docentes_bp)
app.register_blueprint(carreras_bp)
app.register_blueprint(materias_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(pagos_bp)
app.register_blueprint(auditoria_bp)


# ── Manejo global de errores ───────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "message": "Ruta no encontrada"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"success": False, "message": "Método no permitido"}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"success": False, "message": "Error interno del servidor"}), 500


# ── Health check ───────────────────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"success": True, "message": "Backend funcionando correctamente"})


# ── Listado de rutas (útil en desarrollo) ─────────────────────────────────────
@app.route("/api/routes", methods=["GET"])
def list_routes():
    rutas = []
    for rule in app.url_map.iter_rules():
        rutas.append({
            "endpoint": rule.endpoint,
            "methods": sorted(rule.methods - {"HEAD", "OPTIONS"}),
            "url": str(rule),
        })
    return jsonify({"success": True, "data": sorted(rutas, key=lambda x: x["url"])})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}
    app.run(debug=debug, host=os.getenv("FLASK_HOST", "127.0.0.1"), port=5000)
