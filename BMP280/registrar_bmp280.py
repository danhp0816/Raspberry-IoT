import sqlite3  # Importa la librería para gestionar bases de datos SQLite
import os       # Importa la librería para interactuar con el sistema operativo Linux
import board
import adafruit_bmp280
import time

#Configuración de hardware
try:
    i2c = board.I2C()
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)
    print("✅ Sensor BMP280 inicializado correctamente.")
except Exception as e:
    print(f"❌ Error al inicializar el sensor: {e}")
    exit()

def lectura_bmp280():
    try:
        # Intenta establecer una conexión con el archivo físico de la base de datos
        conn = sqlite3.connect('/home/rpi5-dev/Scripts/BMP280/ambiente.db')
        # Crea un 'cursor', que es el objeto que permite ejecutar comandos SQL dentro de la base
        cursor = conn.cursor()
    
        temp = round(sensor.temperature, 2)
        pres = round(sensor.pressure, 2)
    
        # Ejecuta la instrucción pasando los datos reales: nombre, valor y unidad
        cursor.execute("""
            INSERT INTO clima (fecha, temperatura, presion)
            VALUES (datetime('now', 'localtime'),?,?)
        """,(temp,pres))
    
        # Guarda los cambios de forma permanente en el archivo .db (imprescindible en SQLite)
        conn.commit()
        print(f"[{time.strftime('%H:%M:%S')}] Registro guardado -> Temp: {temp}°C | Pres: {pres}hPa")
        conn.close()
    
    except sqlite3.Error as e:
        print(f"❌ Error en la Base de Datos: {e}")
    except Exception as e:
        print(f"❌ Error Inesperado: {e}")
    
# 5. Bucle de ejecución (cada 60 segundos para monitoreo ambiental)
print("🚀 Iniciando monitoreo ambiental... (Presiona Ctrl+C para detener)")
try:
    while True:
        lectura_bmp280()
        time.sleep(90) 
except KeyboardInterrupt:
    print("\n🛑 Monitoreo detenido por el usuario.")

