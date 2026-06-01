from database import get_connection


def _row_to_pago(row) -> dict:
    return {
        "id_pago": row[0],
        "id_inscripcion": row[1],
        "monto": float(row[2]) if row[2] is not None else None,
        "estado": row[3],
        "fecha_pago": str(row[4]) if row[4] else None,
    }


def get_all_pagos() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_pago, id_inscripcion, monto, estado, fecha_pago
        FROM pagos
        ORDER BY ISNULL(fecha_pago, '19000101') DESC, id_pago DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_pago(r) for r in rows]


def create_pago(id_inscripcion: int, monto: float, estado: str = "PENDIENTE",
                fecha_pago: str | None = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    estado = estado.upper()
    fecha_sql = "GETDATE()" if estado == "PAGADO" and not fecha_pago else "?"
    params = [id_inscripcion, monto, estado]
    if fecha_sql == "?":
        params.append(fecha_pago)
    cursor.execute(f"""
        INSERT INTO pagos (id_inscripcion, monto, estado, fecha_pago)
        OUTPUT INSERTED.id_pago
        VALUES (?, ?, ?, {fecha_sql})
    """, params)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_pago": row[0]}


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

    if not sets:
        conn.close()
        return False

    params.append(id_pago)
    cursor.execute(f"UPDATE pagos SET {', '.join(sets)} WHERE id_pago = ?", params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
