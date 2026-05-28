import pyodbc
import os
from config import (
    DB_DRIVER, DB_SERVER, DB_DATABASE,
    DB_TRUSTED_CONNECTION, DB_USER, DB_PASSWORD
)

pyodbc.pooling = True


def get_connection():
    """
    Devuelve una conexión activa a SQL Server.
    Soporta Windows Auth (Trusted_Connection) y SQL Auth (usuario/password).
    """
    if DB_TRUSTED_CONNECTION.lower() == "yes":
        conn_str = (
            f"DRIVER={DB_DRIVER};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"Trusted_Connection=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={DB_DRIVER};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
        )

    timeout = int(os.getenv("DB_TIMEOUT_SECONDS", "5"))
    return pyodbc.connect(conn_str, timeout=timeout)
