from database import get_connection
from models.inscripcion import Inscripcion


def _row_to_inscripcion(row) -> Inscripcion:
    return Inscripcion(
        id_inscripcion=row[0], id_alumno=row[1], id_materia=row[2],
        id_periodo=row[3], estado=row[4], fecha_inscripcion=row[5],
        motivo_baja=row[6] if len(row) > 6 else None,
        fecha_baja=row[7] if len(row) > 7 else None,
        id_pago=row[8] if len(row) > 8 else None,
        monto_pago=row[9] if len(row) > 9 else None,
        estado_pago=row[10] if len(row) > 10 else None,
        fecha_pago=row[11] if len(row) > 11 else None,
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
        SELECT i.id_inscripcion, i.id_alumno, i.id_materia, i.id_periodo,
               i.estado, i.fecha_inscripcion, i.motivo_baja, i.fecha_baja,
               p.id_pago, p.monto, p.estado, p.fecha_pago
        FROM inscripciones i
        OUTER APPLY (
            SELECT TOP 1 id_pago, monto, estado, fecha_pago
            FROM pagos
            WHERE id_inscripcion = i.id_inscripcion
            ORDER BY ISNULL(fecha_pago, '19000101') DESC, id_pago DESC
        ) p
        WHERE i.id_alumno = ?
        ORDER BY i.fecha_inscripcion DESC
    """, (id_alumno,))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_inscripcion(r) for r in rows]


def get_all_inscripciones(id_periodo=None) -> list[Inscripcion]:
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT i.id_inscripcion, i.id_alumno, i.id_materia, i.id_periodo,
               i.estado, i.fecha_inscripcion, i.motivo_baja, i.fecha_baja,
               p.id_pago, p.monto, p.estado, p.fecha_pago
        FROM inscripciones i
        OUTER APPLY (
            SELECT TOP 1 id_pago, monto, estado, fecha_pago
            FROM pagos
            WHERE id_inscripcion = i.id_inscripcion
            ORDER BY ISNULL(fecha_pago, '19000101') DESC, id_pago DESC
        ) p
        WHERE 1=1
    """
    params = []
    if id_periodo:
        sql += " AND i.id_periodo = ?"
        params.append(id_periodo)
    sql += " ORDER BY i.fecha_inscripcion DESC"
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


def update_estado_inscripcion(id_inscripcion: int, estado: str, motivo_baja: str | None = None) -> bool:
    estados_validos = ["PENDIENTE", "ACTIVA", "BAJA", "FINALIZADA"]
    estado = estado.upper()
    if estado not in estados_validos:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_alumno, id_materia, estado FROM inscripciones WHERE id_inscripcion = ?",
            (id_inscripcion,)
        )
        row = cursor.fetchone()
        if not row:
            return False

        if estado in ["PENDIENTE", "ACTIVA"]:
            _validate_inscripcion(cursor, row[0], row[1], exclude_id=id_inscripcion)
            cursor.execute(
                "UPDATE inscripciones SET estado = ?, motivo_baja = NULL, fecha_baja = NULL WHERE id_inscripcion = ?",
                (estado, id_inscripcion)
            )
        elif estado == "BAJA":
            motivo = (motivo_baja or "").strip()
            if not motivo:
                raise ValueError("El motivo de baja es requerido")
            if str(row[2]).upper() == "FINALIZADA":
                raise ValueError("No se puede dar de baja una inscripcion finalizada")
            cursor.execute(
                """
                UPDATE inscripciones
                SET estado = 'BAJA', motivo_baja = ?, fecha_baja = GETDATE()
                WHERE id_inscripcion = ?
                """,
                (motivo, id_inscripcion)
            )
        else:
            if str(row[2]).upper() == "BAJA":
                raise ValueError("No se puede finalizar una inscripcion dada de baja")
            cursor.execute(
                "UPDATE inscripciones SET estado = ? WHERE id_inscripcion = ?",
                (estado, id_inscripcion)
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
