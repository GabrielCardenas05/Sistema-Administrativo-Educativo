from database import get_connection


def get_usuario_by_username(username):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT
            id_usuario,
            usuario,
            password_hash,
            activo
        FROM usuarios
        WHERE usuario = ?
    """

    cursor.execute(query, (username,))

    usuario = cursor.fetchone()

    conn.close()

    return usuario