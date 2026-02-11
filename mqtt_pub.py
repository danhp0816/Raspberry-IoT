import paho.mqtt.client as mqtt #Librería istalada en el entorno virtual
import time
import os

#Configuración deñl BROKER
BROKER = "localhost"
TOPIC = "casa/rpi5/temperatura"

def obtener_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    return res.replace("temp","").replace("'C\n","")

#1. Instancia del Cliente
cliente = mqtt.Client()

#2. Conexión con BROKER local
cliente.connect(BROKER, 1883, 60)

print(f"Iniciando publicación en el tópico: {TOPIC}")

try:
    while True:
        temp=obtener_temp()
        #3. Publicación del mensaje
        cliente.publish(TOPIC, payload=temp,qos=1)
        print(f"Enviado: {temp}°C")
        time.sleep(10) #60 Segundo antes de la siguiente lectura

except KeyboardInterrupt:
    print(f"\nPublicación finalizada por el usuario")
    cliente.disconnect()