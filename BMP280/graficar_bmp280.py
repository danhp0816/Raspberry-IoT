##ESTE SCRIPT TOMA LOS ÚLTIMOS 50 DATOS REGISTRADOS EN ambiente.db y los grafica

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import argparse
import datetime


def generar_grafica_clima(base_datos):
    base_datos = '/home/rpi5-dev/Scripts/BMP280/ambiente.db'
    try:
        # 1. Cargar datos
        conn = sqlite3.connect(base_datos)
        query = "SELECT fecha, temperatura, presion FROM clima ORDER BY fecha DESC LIMIT 50"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("⚠️ No hay datos para graficar.")
            return

        # Convertir fecha a objeto datetime y ordenar cronológicamente
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha')

        # 2. Configurar la figura con dos sub-gráficas (Subplots)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        plt.subplots_adjust(hspace=0.3)

        # --- Gráfica de Temperatura ---
        ax1.plot(df['fecha'], df['temperatura'], color='#FF0000', marker='.', linestyle='-', linewidth=1)
        ax1.set_ylabel('Temperatura (°C)', fontweight='bold')
        ax1.set_title(f'Monitoreo Ambiental', fontsize=14, fontweight='bold')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.tick_params(axis='y', labelcolor='tab:red')

        # --- Gráfica de Presión ---
        ax2.plot(df['fecha'], df['presion'], color='tab:blue', marker='s', linestyle='-', linewidth=2)
        ax2.set_ylabel('Presión (hPa)', fontweight='bold')
        ax2.set_xlabel('Hora de la medición', fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.tick_params(axis='y', labelcolor='tab:blue')

        # Formatear el eje X para que sea legible
        xfmt = mdates.DateFormatter('%H:%M:%S')
        ax2.xaxis.set_major_formatter(xfmt)
        plt.xticks(rotation=45)

        # 3. Guardar la imagen
        path_salida = 'static/temp_ambiente.png'
        plt.savefig(path_salida, bbox_inches='tight')
        plt.close()
        print(f"✅ Gráfica doble generada en: {path_salida}")
        
    except Exception as e:
        print(f"❌ Error al graficar: {e}")

if __name__ == "__main__":
    # Prueba rápida: asegúrate de que la ruta coincida con tu nueva DB
    generar_grafica_clima('/home/rpi5-dev/Scripts/BMP280/ambiente.db')
