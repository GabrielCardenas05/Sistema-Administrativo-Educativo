from database import get_connection
from models.carrera import Carrera


def _row_to_carrera(row) -> Carrera:
    return Carrera(id_carrera=row[0], nombre=row[1], activa=row[2])


def get_all_carreras(solo_activas=False) -> list[Carrera]:
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id_carrera, nombre, activa FROM carreras"
    if solo_activas:
        sql += " WHERE activa = 1"
    sql += " ORDER BY nombre"
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_carrera(r) for r in rows]


def get_carrera_by_id(id_carrera: int) -> Carrera | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_carrera, nombre, activa FROM carreras WHERE id_carrera = ?", (id_carrera,))
    row = cursor.fetchone()
    conn.close()
    return _row_to_carrera(row) if row else None


def create_carrera(nombre: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO carreras (nombre, activa) OUTPUT INSERTED.id_carrera VALUES (?, 1)",
        (nombre,)
    )
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_carrera": row[0], "nombre": nombre}


def update_carrera(id_carrera: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    sets, params = [], []
    for campo in ["nombre", "activa"]:
        if campo in data:
            sets.append(f"{campo} = ?")
            params.append(data[campo])
    if not sets:
        conn.close()
        return False
    params.append(id_carrera)
    cursor.execute(f"UPDATE carreras SET {', '.join(sets)} WHERE id_carrera = ?", params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_carrera(id_carrera: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM carreras WHERE id_carrera = ?", (id_carrera,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
