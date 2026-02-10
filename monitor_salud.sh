#!/bin/bash

# --- Definición de variables ---
FECHA=$(date '+%Y-%m-%d %H:%M:%S')
TEMP=$(vcgencmd measure_temp | cut -d "=" -f2)
CPU_LOAD=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
RAM_USO=$(free -m | awk '/Mem:/ { printf("%.2f%%", $3/$2*100) }')
DISCO=$(df -h / | awk '/\// {print $5}')

# --- Formato de salida para la consola ---
echo "------------------------------------------"
echo "REPORTE DE SALUD - $FECHA"
echo "------------------------------------------"
echo "Temperatura CPU : $TEMP"
echo "Carga de CPU    : $CPU_LOAD%"
echo "Uso de RAM      : $RAM_USO"
echo "Espacio Disco   : $DISCO"
echo "------------------------------------------"

# --- Guardar en un archivo LOG (Trazabilidad) ---
echo "$FECHA | Temp: $TEMP | CPU: $CPU_LOAD% | RAM: $RAM_USO | Disco: $DISCO" >> ~/Scripts/log_salud.txt
