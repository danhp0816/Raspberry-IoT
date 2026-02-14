import board
import adafruit_bmp280

# Configuración del bus I2C
i2c = board.I2C() 
# Usamos la dirección 0x77 que detectamos en tu terminal
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

print(f"Temperatura: {sensor.temperature:.2f} °C")
print(f"Presión: {sensor.pressure:.2f} hPa")
