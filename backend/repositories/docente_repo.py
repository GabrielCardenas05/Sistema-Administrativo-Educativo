from database import get_connection
from models.docente import Docente


def _row_to_docente(row) -> Docente:
    return Docente(id_docente=row[0], id_usuario=row[1], nombre=row[2], especialidad=row[3])


def get_all_docentes() -> list[Docente]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_docente, id_usuario, nombre, especialidad FROM docentes ORDER BY nombre")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_docente(r) for r in rows]


def get_docente_by_id(id_docente: int) -> Docente | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_docente, id_usuario, nombre, especialidad FROM docentes WHERE id_docente = ?",
        (id_docente,)
    )
    row = cursor.fetchone()
    conn.close()
    return _row_to_docente(row) if row else None


def create_docente(id_usuario: int, nombre: str, especialidad: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO docentes (id_usuario, nombre, especialidad)
        OUTPUT INSERTED.id_docente
        VALUES (?, ?, ?)
    """, (id_usuario, nombre, especialidad))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_docente": row[0], "nombre": nombre}


def update_docente(id_docente: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    sets, params = [], []
    for campo in ["nombre", "especialidad"]:
        if campo in data:
            sets.append(f"{campo} = ?")
            params.append(data[campo])
    if not sets:
        conn.close()
        return False
    params.append(id_docente)
    cursor.execute(f"UPDATE docentes SET {', '.join(sets)} WHERE id_docente = ?", params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_docente(id_docente: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM docentes WHERE id_docente = ?", (id_docente,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
