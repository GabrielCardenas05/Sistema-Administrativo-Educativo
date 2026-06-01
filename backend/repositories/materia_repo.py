from database import get_connection
from models.materia import Materia


def _row_to_materia(row) -> Materia:
    return Materia(
        id_materia=row[0], clave=row[1], nombre=row[2],
        id_carrera=row[3], semestre=row[4], cupo=row[5], activa=row[6]
    )


def _attach_docentes(cursor, materias: list[Materia]) -> None:
    if not materias:
        return
    cursor.execute("SELECT OBJECT_ID('materia_docente', 'U')")
    if not cursor.fetchone()[0]:
        return
    ids = [m.id_materia for m in materias]
    placeholders = ",".join("?" for _ in ids)
    cursor.execute(f"""
        SELECT md.id_materia, d.id_docente, d.nombre, d.especialidad
        FROM materia_docente md
        INNER JOIN docentes d ON d.id_docente = md.id_docente
        WHERE md.id_materia IN ({placeholders})
        ORDER BY d.nombre
    """, ids)
    docentes_por_materia = {id_materia: [] for id_materia in ids}
    for row in cursor.fetchall():
        docentes_por_materia.setdefault(row[0], []).append({
            "id_docente": row[1],
            "nombre": row[2],
            "especialidad": row[3],
        })
    for materia in materias:
        materia.docentes = docentes_por_materia.get(materia.id_materia, [])


def get_all_materias(id_carrera=None, semestre=None) -> list[Materia]:
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id_materia, clave, nombre, id_carrera, semestre, cupo, activa FROM materias WHERE 1=1"
    params = []
    if id_carrera:
        sql += " AND id_carrera = ?"
        params.append(id_carrera)
    if semestre:
        sql += " AND semestre = ?"
        params.append(semestre)
    sql += " ORDER BY nombre"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    materias = [_row_to_materia(r) for r in rows]
    _attach_docentes(cursor, materias)
    conn.close()
    return materias


def get_materia_by_id(id_materia: int) -> Materia | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_materia, clave, nombre, id_carrera, semestre, cupo, activa FROM materias WHERE id_materia = ?",
        (id_materia,)
    )
    row = cursor.fetchone()
    materia = _row_to_materia(row) if row else None
    if materia:
        _attach_docentes(cursor, [materia])
    conn.close()
    return materia


def create_materia(clave: str, nombre: str, id_carrera: int, semestre: int, cupo: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materias (clave, nombre, id_carrera, semestre, cupo, activa)
        OUTPUT INSERTED.id_materia
        VALUES (?, ?, ?, ?, ?, 1)
    """, (clave, nombre, id_carrera, semestre, cupo))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_materia": row[0], "clave": clave, "nombre": nombre}


def update_materia(id_materia: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    sets, params = [], []
    for campo in ["clave", "nombre", "id_carrera", "semestre", "cupo", "activa"]:
        if campo in data:
            sets.append(f"{campo} = ?")
            params.append(data[campo])
    if not sets:
        conn.close()
        return False
    params.append(id_materia)
    cursor.execute(f"UPDATE materias SET {', '.join(sets)} WHERE id_materia = ?", params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_materia(id_materia: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materias WHERE id_materia = ?", (id_materia,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
