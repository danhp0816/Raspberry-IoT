import sqlite3  # Importa la librería para gestionar bases de datos SQLite
import os       # Importa la librería para interactuar con el sistema operativo Linux

def obtener_temp():
    # Ejecuta el comando de terminal 'vcgencmd' y lee la primera línea de la respuesta
    res = os.popen("vcgencmd measure_temp").readline()
    
    # Limpia la cadena (quita "temp=" y "'C\n") y convierte el texto restante a número decimal (float)
    return float(res.replace("temp=",'').replace("'C\n",""))

try:
    # Intenta establecer una conexión con el archivo físico de la base de datos
    conn = sqlite3.connect('/home/rpi5-dev/Scripts/sensores.db')
    
    # Crea un 'cursor', que es el objeto que permite ejecutar comandos SQL dentro de la base
    cursor = conn.cursor()
    
    # Llama a nuestra función de arriba para obtener la temperatura real del procesador
    temp_actual = obtener_temp()
    
    # Prepara la instrucción SQL. Los '?' son marcadores de posición por seguridad (evitan inyecciones SQL)
    sql = "INSERT INTO lecturas (sensor_nombre, temperatura, unidad) VALUES (?, ?, ?)"
    
    # Ejecuta la instrucción pasando los datos reales: nombre, valor y unidad
    cursor.execute(sql, ('CPU_INTERNAL', temp_actual, 'C'))
    
    # Guarda los cambios de forma permanente en el archivo .db (imprescindible en SQLite)
    conn.commit()
    
    # Imprime una confirmación en la terminal de VS Code para el operador
    print(f"Registro exitoso: {temp_actual}°C guardados en la base de datos.")
    
    # Cierra la conexión para liberar el archivo y evitar que se bloquee
    conn.close()

except Exception as e:
    # Si ocurre cualquier error (archivo no encontrado, tabla inexistente, etc.), lo captura y lo muestra
    print(f"Error detectado durante la operación: {e}") #PRUEBA 1