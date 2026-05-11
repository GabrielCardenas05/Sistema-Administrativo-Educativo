from database import get_connection

try:
    conn = get_connection()
    print("Conexion exitosa")
    conn.close()

except Exception as e:
    print("Error:", e)
    
