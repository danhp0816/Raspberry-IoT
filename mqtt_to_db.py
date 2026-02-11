import sqlite3  # Importa la librería para gestionar bases de datos SQLite
import os       # Importa la librería para interactuar con el sistema operativo Linux
import paho.mqtt.client as mqtt #Librería istalada en el entorno virtual
import time

#Configuración deñl BROKER
BROKER = "localhost"
TOPIC = "casa/rpi5/temperatura"

def obtener_temp():
    # Ejecuta el comando de terminal 'vcgencmd' y lee la primera línea de la respuesta
    res = os.popen("vcgencmd measure_temp").readline()
     # Limpia la cadena y convierte el texto restante a número decimal (float)
    return res.replace("temp","").replace("'C\n","")

#1. Instancia del Cliente
cliente = mqtt.Client()

#2. Conexión con BROKER local
cliente.connect(BROKER, 1883, 60)
print(f"Iniciando publicación en el tópico: {TOPIC}")

def registrar_lecturas(valor_temp):
    conn = sqlite3.connect('/home/rpi5-dev/Scripts/sensores.db')
    
    # Crea un 'cursor', que es el objeto que permite ejecutar comandos SQL dentro de la base
    cursor = conn.cursor()
    
    # Prepara la instrucción SQL. Los '?' son marcadores de posición por seguridad (evitan inyecciones SQL)
    sql = "INSERT INTO lecturas (sensor_nombre, temperatura, unidad) VALUES (?, ?, ?)"
    
    # Ejecuta la instrucción pasando los datos reales: nombre, valor y unidad
    cursor.execute(sql, ('CPU_INTERNAL', valor_temp, 'C'))
    
    # Guarda los cambios de forma permanente en el archivo .db (imprescindible en SQLite)
    conn.commit()
    
    # Imprime una confirmación en la terminal de VS Code para el operador
    print(f"Registro exitoso: {valor_temp}°C guardados en la base de datos.")

    # Cierra la conexión para liberar el archivo y evitar que se bloquee
    conn.close()

#Programa principal
try:
        while True:
            temp=obtener_temp() #Función que conecta con el OS de Rpi5 para obtener la temperatura
            #3. Publicación del mensaje
            cliente.publish(TOPIC, payload=temp,qos=1)
            registrar_lecturas(temp)#Función que recolecta la información y la registra en la tabla
            time.sleep(20) #Tiempo de espewra entre mediciones y registros
           

except KeyboardInterrupt:
    print(f"\nPublicación finalizada por el usuario")
    cliente.disconnect()        