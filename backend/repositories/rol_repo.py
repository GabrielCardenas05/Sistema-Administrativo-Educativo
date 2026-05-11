from database import get_connection


def get_roles_by_user_id(id_usuario):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            r.id_rol,
            r.nombre
        FROM Usuario_Rol ur
        INNER JOIN roles r
            ON ur.id_rol = r.id_rol
        WHERE ur.id_usuario = ?
    """

    cursor.execute(query, (id_usuario,))

    roles = cursor.fetchall()

    conn.close()

    return roles