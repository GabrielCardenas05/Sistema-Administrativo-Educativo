from database import get_connection
from models.usuario import Usuario
from utils.security import hash_password


def _row_to_usuario(row) -> Usuario:
    return Usuario(
        id_usuario=row[0],
        usuario=row[1],
        password_hash=row[2],
        activo=row[3],
    )


def get_all_usuarios() -> list[Usuario]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, usuario, password_hash, activo FROM usuarios ORDER BY id_usuario")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_usuario(r) for r in rows]


def get_usuario_by_id(id_usuario: int) -> Usuario | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_usuario, usuario, password_hash, activo FROM usuarios WHERE id_usuario = ?",
        (id_usuario,)
    )
    row = cursor.fetchone()
    conn.close()
    return _row_to_usuario(row) if row else None


def get_usuario_by_username(username: str) -> Usuario | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_usuario, usuario, password_hash, activo FROM usuarios WHERE usuario = ?",
        (username,)
    )
    row = cursor.fetchone()
    conn.close()
    return _row_to_usuario(row) if row else None


def create_usuario(usuario: str, password: str, roles: list[str]) -> dict:
    """
    Crea un usuario y le asigna los roles indicados.
    roles: lista de nombres de rol, e.g. ["ALUMNO"]
    """
    conn = get_connection()
    cursor = conn.cursor()

    normalized_roles = [str(r).upper() for r in roles]
    if not normalized_roles:
        conn.close()
        raise ValueError("Debe asignarse al menos un rol")

    placeholders = ",".join("?" for _ in normalized_roles)
    cursor.execute(
        f"SELECT id_rol, UPPER(nombre) FROM roles WHERE UPPER(nombre) IN ({placeholders})",
        normalized_roles,
    )
    role_rows = cursor.fetchall()
    role_map = {row[1]: row[0] for row in role_rows}
    missing_roles = sorted(set(normalized_roles) - set(role_map))
    if missing_roles:
        conn.close()
        raise ValueError(f"Roles invalidos: {', '.join(missing_roles)}")

    try:
        password_hashed = hash_password(password)
        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password_hash, activo, created_at, updated_at)
            OUTPUT INSERTED.id_usuario
            VALUES (?, ?, 1, GETDATE(), GETDATE())
            """,
            (usuario, password_hashed)
        )
        row = cursor.fetchone()
        id_usuario = row[0]

        for nombre_rol in normalized_roles:
            cursor.execute(
                "INSERT INTO Usuario_Rol (id_usuario, id_rol) VALUES (?, ?)",
                (id_usuario, role_map[nombre_rol])
            )

        conn.commit()
        return {"id_usuario": id_usuario, "usuario": usuario}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_usuario(id_usuario: int, data: dict) -> bool:
    """
    Actualiza usuario (campos opcionales: usuario, password, activo).
    """
    conn = get_connection()
    cursor = conn.cursor()

    sets = []
    params = []

    if "usuario" in data:
        sets.append("usuario = ?")
        params.append(data["usuario"])
    if "password" in data:
        sets.append("password_hash = ?")
        params.append(hash_password(data["password"]))
    if "activo" in data:
        sets.append("activo = ?")
        params.append(1 if data["activo"] else 0)

    if not sets:
        conn.close()
        return False

    sets.append("updated_at = GETDATE()")
    params.append(id_usuario)

    sql = f"UPDATE usuarios SET {', '.join(sets)} WHERE id_usuario = ?"
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def delete_usuario(id_usuario: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    # Primero borra relación de roles
    cursor.execute("DELETE FROM Usuario_Rol WHERE id_usuario = ?", (id_usuario,))
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def get_roles_by_user_id(id_usuario: int) -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.nombre FROM Usuario_Rol ur
        INNER JOIN roles r ON ur.id_rol = r.id_rol
        WHERE ur.id_usuario = ?
        """,
        (id_usuario,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [r[0].upper() for r in rows]
