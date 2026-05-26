from database import get_connection
from models.inscripcion import Inscripcion


def _row_to_inscripcion(row) -> Inscripcion:
    return Inscripcion(
        id_inscripcion=row[0], id_alumno=row[1], id_materia=row[2],
        id_periodo=row[3], estado=row[4], fecha_inscripcion=row[5]
    )


def _validate_inscripcion(cursor, id_alumno: int, id_materia: int, exclude_id: int | None = None) -> None:
    cursor.execute("""
        SELECT id_carrera, semestre, estatus
        FROM alumnos
        WHERE id_alumno = ?
    """, (id_alumno,))
    alumno = cursor.fetchone()
    if not alumno:
        raise ValueError("Alumno no encontrado")
    if str(alumno[2]).upper() != "ACTIVO":
        raise ValueError("El alumno no esta activo")

    cursor.execute("""
        SELECT id_carrera, semestre, cupo, activa
        FROM materias
        WHERE id_materia = ?
    """, (id_materia,))
    materia = cursor.fetchone()
    if not materia:
        raise ValueError("Materia no encontrada")
    if not bool(materia[3]):
        raise ValueError("La materia no esta activa")
    if alumno[0] != materia[0] or alumno[1] != materia[1]:
        raise ValueError("La materia no corresponde a la carrera o semestre del alumno")

    sql = """
        SELECT COUNT(*)
        FROM inscripciones
        WHERE id_materia = ?
          AND estado IN ('PENDIENTE', 'ACTIVA')
    """
    params = [id_materia]
    if exclude_id:
        sql += " AND id_inscripcion <> ?"
        params.append(exclude_id)
    cursor.execute(sql, params)
    inscritos = cursor.fetchone()[0]
    if inscritos >= materia[2]:
        raise ValueError("No hay cupo disponible para la materia")


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
    try:
        _validate_inscripcion(cursor, id_alumno, id_materia)
        cursor.execute("""
            INSERT INTO inscripciones (id_alumno, id_materia, id_periodo, estado, fecha_inscripcion)
            OUTPUT INSERTED.id_inscripcion
            VALUES (?, ?, ?, 'PENDIENTE', GETDATE())
        """, (id_alumno, id_materia, id_periodo))
        row = cursor.fetchone()
        conn.commit()
        return {"id_inscripcion": row[0]}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_estado_inscripcion(id_inscripcion: int, estado: str) -> bool:
    estados_validos = ["PENDIENTE", "ACTIVA", "BAJA", "FINALIZADA"]
    if estado.upper() not in estados_validos:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if estado.upper() in ["PENDIENTE", "ACTIVA"]:
            cursor.execute(
                "SELECT id_alumno, id_materia FROM inscripciones WHERE id_inscripcion = ?",
                (id_inscripcion,)
            )
            row = cursor.fetchone()
            if not row:
                return False
            _validate_inscripcion(cursor, row[0], row[1], exclude_id=id_inscripcion)
        cursor.execute(
            "UPDATE inscripciones SET estado = ? WHERE id_inscripcion = ?",
            (estado.upper(), id_inscripcion)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_inscripcion(id_inscripcion: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inscripciones WHERE id_inscripcion = ?", (id_inscripcion,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
