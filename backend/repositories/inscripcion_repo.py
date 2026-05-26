from database import get_connection
from models.inscripcion import Inscripcion


def _row_to_inscripcion(row) -> Inscripcion:
    return Inscripcion(
        id_inscripcion=row[0], id_alumno=row[1], id_materia=row[2],
        id_periodo=row[3], estado=row[4], fecha_inscripcion=row[5]
    )


def get_inscripciones_by_alumno(id_alumno: int) -> list[Inscripcion]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_inscripcion, id_alumno, id_materia, id_periodo, estado, fecha_inscripcion
        FROM inscripciones WHERE id_alumno = ?
        ORDER BY fecha_inscripcion DESC
    """, (id_alumno,))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_inscripcion(r) for r in rows]


def get_all_inscripciones(id_periodo=None) -> list[Inscripcion]:
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT id_inscripcion, id_alumno, id_materia, id_periodo, estado, fecha_inscripcion
        FROM inscripciones WHERE 1=1
    """
    params = []
    if id_periodo:
        sql += " AND id_periodo = ?"
        params.append(id_periodo)
    sql += " ORDER BY fecha_inscripcion DESC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_inscripcion(r) for r in rows]


def create_inscripcion(id_alumno: int, id_materia: int, id_periodo: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inscripciones (id_alumno, id_materia, id_periodo, estado, fecha_inscripcion)
        OUTPUT INSERTED.id_inscripcion
        VALUES (?, ?, ?, 'PENDIENTE', GETDATE())
    """, (id_alumno, id_materia, id_periodo))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_inscripcion": row[0]}


def update_estado_inscripcion(id_inscripcion: int, estado: str) -> bool:
    estados_validos = ["PENDIENTE", "ACTIVA", "BAJA", "FINALIZADA"]
    if estado.upper() not in estados_validos:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE inscripciones SET estado = ? WHERE id_inscripcion = ?",
        (estado.upper(), id_inscripcion)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_inscripcion(id_inscripcion: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inscripciones WHERE id_inscripcion = ?", (id_inscripcion,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
