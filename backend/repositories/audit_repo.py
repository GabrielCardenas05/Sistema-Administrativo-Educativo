from database import get_connection


def _row_to_log(row) -> dict:
    return {
        "id_log": row[0],
        "id_usuario": row[1],
        "usuario": row[2],
        "accion": row[3],
        "descripcion": row[4],
        "fecha": str(row[5]) if row[5] else None,
    }


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


def get_audit_logs(limit: int = 200) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT TOP ({int(limit)}) l.id_log, l.id_usuario, u.usuario, l.accion, l.descripcion, l.fecha
        FROM logs_auditoria l
        INNER JOIN usuarios u ON u.id_usuario = l.id_usuario
        ORDER BY l.fecha DESC, l.id_log DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_log(r) for r in rows]
