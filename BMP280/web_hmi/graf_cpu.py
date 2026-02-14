import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def generar_reporte_cpu(db_path, fecha=None, h_ini="00:00:00", h_fin="23:59:59"):
    try:
        if not os.path.exists(db_path):
            print(f"❌ DB CPU no encontrada en: {db_path}")
            return False

        conn = sqlite3.connect(db_path)
        
        # Filtro por fecha y hora
        if fecha:
            query = f"""SELECT fecha, temperatura FROM lecturas 
                       WHERE fecha BETWEEN '{fecha} {h_ini}' AND '{fecha} {h_fin}' 
                       ORDER BY fecha ASC"""
        else:
            query = "SELECT fecha, temperatura FROM lecturas ORDER BY fecha DESC LIMIT 60"
        
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return False

        # Convertir fecha a datetime
        df['fecha'] = pd.to_datetime(df['fecha'])

        # 1. Crear figura con 2 paneles
        fig, ax = plt.subplots(figsize=(12, 6))

        # --- PANEL INFERIOR: TEMPERATURA DEL CPU ---
        ax.plot(df['fecha'], df['temperatura'], color='tab:orange', linewidth=2, label='Temp CPU')
        ax.set_ylabel('Temp (°C)', color='tab:orange', fontsize=12)
        ax.set_xlabel('Tiempo', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)

        # 2. Formatear el eje X (Tiempo)
        xfmt = mdates.DateFormatter('%H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        fig.autofmt_xdate()

        plt.tight_layout()
        
        # 3. Guardar imagen
        plt.savefig('static/reporte_cpu.png')
        plt.close()
        return True

    except Exception as e:
        print(f"❌ Error en reporte_cpu: {e}")
        return False