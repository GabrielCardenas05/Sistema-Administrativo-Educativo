from database import get_connection


def log_audit(id_usuario: int, accion: str, descripcion: str = "") -> None:
    """Registra auditoria sin bloquear la operacion principal si falla."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO logs_auditoria (id_usuario, accion, descripcion, fecha)
            VALUES (?, ?, ?, GETDATE())
            """,
            (id_usuario, accion[:100], descripcion),
        )
        conn.commit()
    except Exception:
        pass
    finally:
        if conn:
            conn.close()
