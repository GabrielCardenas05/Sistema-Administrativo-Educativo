from database import get_connection


def _row_to_ticket(row) -> dict:
    return {
        "id_ticket": row[0],
        "id_usuario": row[1],
        "usuario": row[2],
        "tipo": row[3],
        "titulo": row[4],
        "descripcion": row[5],
        "estatus": row[6],
        "prioridad": row[7],
        "id_inscripcion": row[8],
        "fecha_creacion": str(row[9]) if row[9] else None,
        "fecha_actualizacion": str(row[10]) if row[10] else None,
    }


def _base_query() -> str:
    return """
        SELECT t.id_ticket, t.id_usuario, u.usuario, t.tipo, t.titulo,
               t.descripcion, t.estatus, t.prioridad, t.id_inscripcion,
               t.fecha_creacion, t.fecha_actualizacion
        FROM tickets_soporte t
        INNER JOIN usuarios u ON u.id_usuario = t.id_usuario
    """


def get_all_tickets() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(_base_query() + " ORDER BY t.fecha_creacion DESC")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_ticket(r) for r in rows]


def get_tickets_by_usuario(id_usuario: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        _base_query() + " WHERE t.id_usuario = ? ORDER BY t.fecha_creacion DESC",
        (id_usuario,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_ticket(r) for r in rows]


def create_ticket(id_usuario: int, tipo: str, titulo: str, descripcion: str,
                  prioridad: str = "MEDIA", id_inscripcion: int | None = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets_soporte (
            id_usuario, tipo, titulo, descripcion, estatus,
            prioridad, id_inscripcion, fecha_creacion, fecha_actualizacion
        )
        OUTPUT INSERTED.id_ticket
        VALUES (?, ?, ?, ?, 'ABIERTO', ?, ?, GETDATE(), GETDATE())
    """, (id_usuario, tipo, titulo, descripcion, prioridad, id_inscripcion))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_ticket": row[0]}


def update_ticket_status(id_ticket: int, estatus: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tickets_soporte
        SET estatus = ?, fecha_actualizacion = GETDATE()
        WHERE id_ticket = ?
    """, (estatus, id_ticket))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def inscripcion_belongs_to_usuario(id_inscripcion: int, id_usuario: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1
        FROM inscripciones i
        INNER JOIN alumnos a ON a.id_alumno = i.id_alumno
        WHERE i.id_inscripcion = ? AND a.id_usuario = ?
    """, (id_inscripcion, id_usuario))
    row = cursor.fetchone()
    conn.close()
    return bool(row)
