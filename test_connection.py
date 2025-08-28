import mysql.connector

conn = None  # Initialize to handle errors

# Data extracted from the URL
host = "switchback.proxy.rlwy.net"
port = 40842
user = "root"
password = "hpDkeofzJSiakVbpmozJZVMSpUCbIOca"
database = "railway"

try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    print("Conexión exitosa a MySQL en Railway")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    print("Tablas:", cursor.fetchall())

except mysql.connector.Error as err:
    print(f"Error de conexión: {err}")

finally:
    if conn and conn.is_connected():
        conn.close()
        print("Conexión cerrada")
