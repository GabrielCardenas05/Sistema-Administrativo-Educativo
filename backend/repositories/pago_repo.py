from uuid import uuid4

from database import get_connection
from repositories.inscripcion_repo import create_or_get_student_inscripcion


def _row_to_pago(row) -> dict:
    pago = {
        "id_pago": row[0],
        "id_inscripcion": row[1],
        "monto": float(row[2]) if row[2] is not None else None,
        "estado": row[3],
        "fecha_pago": str(row[4]) if row[4] else None,
        "metodo_pago": row[5] if len(row) > 5 else None,
        "titular": row[6] if len(row) > 6 else None,
        "tarjeta_ultimos4": row[7] if len(row) > 7 else None,
        "referencia": row[8] if len(row) > 8 else None,
        "concepto": row[9] if len(row) > 9 else None,
        "fecha_creacion": str(row[10]) if len(row) > 10 and row[10] else None,
    }
    if len(row) > 18:
        pago.update({
            "estado_inscripcion": row[11],
            "id_periodo": row[12],
            "id_alumno": row[13],
            "matricula": row[14],
            "alumno": row[15],
            "id_materia": row[16],
            "clave_materia": row[17],
            "materia": row[18],
        })
    return pago


def _new_reference(prefix: str = "SAE") -> str:
    return f"{prefix}-{uuid4().hex[:10].upper()}"


def get_all_pagos() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_pago, p.id_inscripcion, p.monto, p.estado, p.fecha_pago,
               p.metodo_pago, p.titular, p.tarjeta_ultimos4, p.referencia,
               p.concepto, p.fecha_creacion,
               i.estado, i.id_periodo,
               a.id_alumno, a.matricula, a.nombre,
               m.id_materia, m.clave, m.nombre
        FROM pagos p
        INNER JOIN inscripciones i ON i.id_inscripcion = p.id_inscripcion
        INNER JOIN alumnos a ON a.id_alumno = i.id_alumno
        INNER JOIN materias m ON m.id_materia = i.id_materia
        ORDER BY ISNULL(p.fecha_pago, '19000101') DESC, p.id_pago DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_pago(r) for r in rows]


def create_pago(id_inscripcion: int, monto: float, estado: str = "PENDIENTE",
                fecha_pago: str | None = None, metodo_pago: str = "TARJETA",
                titular: str | None = None, tarjeta_ultimos4: str | None = None,
                referencia: str | None = None, concepto: str | None = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    estado = estado.upper()
    metodo_pago = (metodo_pago or "TARJETA").upper()
    referencia = referencia or _new_reference("PAY")
    concepto = concepto or "Pago de inscripcion"
    fecha_sql = "GETDATE()" if estado == "PAGADO" and not fecha_pago else "?"
    params = [
        id_inscripcion, monto, estado, metodo_pago,
        titular, tarjeta_ultimos4, referencia, concepto,
    ]
    if fecha_sql == "?":
        params.append(fecha_pago)
    cursor.execute(f"""
        INSERT INTO pagos (
            id_inscripcion, monto, estado, metodo_pago, titular,
            tarjeta_ultimos4, referencia, concepto, fecha_pago, fecha_creacion
        )
        OUTPUT INSERTED.id_pago
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, {fecha_sql}, GETDATE())
    """, params)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_pago": row[0], "referencia": referencia}


def get_pagos_by_usuario(id_usuario: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_pago, p.id_inscripcion, p.monto, p.estado, p.fecha_pago,
               p.metodo_pago, p.titular, p.tarjeta_ultimos4, p.referencia,
               p.concepto, p.fecha_creacion,
               i.estado, i.id_periodo,
               a.id_alumno, a.matricula, a.nombre,
               m.id_materia, m.clave, m.nombre
        FROM pagos p
        INNER JOIN inscripciones i ON i.id_inscripcion = p.id_inscripcion
        INNER JOIN alumnos a ON a.id_alumno = i.id_alumno
        INNER JOIN materias m ON m.id_materia = i.id_materia
        WHERE a.id_usuario = ?
        ORDER BY ISNULL(p.fecha_pago, p.fecha_creacion) DESC, p.id_pago DESC
    """, (id_usuario,))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_pago(r) for r in rows]


def create_pago_for_student(id_usuario: int, id_materia: int, titular: str,
                            tarjeta_ultimos4: str, monto: float = 1500.00) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    referencia = _new_reference("CMP")
    try:
        id_inscripcion = create_or_get_student_inscripcion(cursor, id_usuario, id_materia)
        cursor.execute("""
            SELECT TOP 1 id_pago
            FROM pagos
            WHERE id_inscripcion = ? AND UPPER(estado) = 'PAGADO'
            ORDER BY fecha_pago DESC, id_pago DESC
        """, (id_inscripcion,))
        if cursor.fetchone():
            raise ValueError("Esta inscripción ya tiene un pago aprobado")

        cursor.execute("""
            INSERT INTO pagos (
                id_inscripcion, monto, estado, metodo_pago, titular,
                tarjeta_ultimos4, referencia, concepto, fecha_pago, fecha_creacion
            )
            OUTPUT INSERTED.id_pago, INSERTED.fecha_pago
            VALUES (?, ?, 'PAGADO', 'TARJETA', ?, ?, ?, 'Inscripcion de materia', GETDATE(), GETDATE())
        """, (id_inscripcion, monto, titular, tarjeta_ultimos4, referencia))
        row = cursor.fetchone()
        conn.commit()
        return {
            "id_pago": row[0],
            "id_inscripcion": id_inscripcion,
            "monto": monto,
            "estado": "PAGADO",
            "fecha_pago": str(row[1]) if row[1] else None,
            "metodo_pago": "TARJETA",
            "titular": titular,
            "tarjeta_ultimos4": tarjeta_ultimos4,
            "referencia": referencia,
            "concepto": "Inscripcion de materia",
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_pago(id_pago: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    sets, params = [], []

    if "monto" in data:
        sets.append("monto = ?")
        params.append(data["monto"])
    if "estado" in data:
        sets.append("estado = ?")
        params.append(str(data["estado"]).upper())
    if "fecha_pago" in data:
        sets.append("fecha_pago = ?")
        params.append(data["fecha_pago"] or None)
    for campo in ["metodo_pago", "titular", "tarjeta_ultimos4", "referencia", "concepto"]:
        if campo in data:
            sets.append(f"{campo} = ?")
            params.append(data[campo])

    if not sets:
        conn.close()
        return False

    params.append(id_pago)
    cursor.execute(f"UPDATE pagos SET {', '.join(sets)} WHERE id_pago = ?", params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
