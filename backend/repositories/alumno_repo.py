from database import get_connection
from models.alumno import Alumno


def _row_to_alumno(row) -> Alumno:
    return Alumno(
        id_alumno=row[0],
        id_usuario=row[1],
        matricula=row[2],
        nombre=row[3],
        curp=row[4],
        id_carrera=row[5],
        semestre=row[6],
        estatus=row[7],
    )


def get_all_alumnos() -> list[Alumno]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id_alumno, a.id_usuario, a.matricula, a.nombre, a.curp,
               a.id_carrera, a.semestre, a.estatus
        FROM alumnos a
        ORDER BY a.nombre
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_alumno(r) for r in rows]


def get_alumno_by_id(id_alumno: int) -> Alumno | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_alumno, id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus
        FROM alumnos WHERE id_alumno = ?
    """, (id_alumno,))
    row = cursor.fetchone()
    conn.close()
    return _row_to_alumno(row) if row else None


def get_alumno_by_usuario_id(id_usuario: int) -> Alumno | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_alumno, id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus
        FROM alumnos WHERE id_usuario = ?
    """, (id_usuario,))
    row = cursor.fetchone()
    conn.close()
    return _row_to_alumno(row) if row else None


def get_alumno_by_matricula(matricula: str) -> Alumno | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_alumno, id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus
        FROM alumnos WHERE matricula = ?
    """, (matricula,))
    row = cursor.fetchone()
    conn.close()
    return _row_to_alumno(row) if row else None


def create_alumno(id_usuario: int, matricula: str, nombre: str, curp: str,
                  id_carrera: int, semestre: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alumnos (id_usuario, matricula, nombre, curp, id_carrera, semestre, estatus)
        OUTPUT INSERTED.id_alumno
        VALUES (?, ?, ?, ?, ?, ?, 'ACTIVO')
    """, (id_usuario, matricula, nombre, curp, id_carrera, semestre))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return {"id_alumno": row[0], "matricula": matricula, "nombre": nombre}


def update_alumno(id_alumno: int, data: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    sets, params = [], []

    campos = ["matricula", "nombre", "curp", "id_carrera", "semestre", "estatus"]
    for campo in campos:
        if campo in data:
            sets.append(f"{campo} = ?")
            params.append(data[campo])

    if not sets:
        conn.close()
        return False

    params.append(id_alumno)
    cursor.execute(f"UPDATE alumnos SET {', '.join(sets)} WHERE id_alumno = ?", params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_alumno(id_alumno: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id_alumno = ?", (id_alumno,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
