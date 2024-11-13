import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
servername = "localhost"
username = "root"
password = ""
dbname = "league_of_legends"

try:
    # Crear la conexión
    conn = mysql.connector.connect(
        host=servername,
        user=username,
        password=password,
        database=dbname
    )

    # Verificar la conexión
    if conn.is_connected():
        print("Conexión exitosa")

except Error as e:
    print("Error en la conexión:", e)

finally:
    # Cerrar la conexión
    if conn.is_connected():
        conn.close()
        print("Conexión cerrada")
