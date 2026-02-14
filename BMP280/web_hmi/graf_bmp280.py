import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generar_reporte_ambiental(db_path, fecha=None, h_ini="00:00:00", h_fin="23:59:59"):
    try:
        conn = sqlite3.connect(db_path)
        # Si hay fecha, filtramos. Si no, traemos los últimos 50 registros.
        if fecha:
            query = f"SELECT * FROM clima WHERE fecha BETWEEN '{fecha} {h_ini}' AND '{fecha} {h_fin}' ORDER BY fecha ASC"
        else:
            query = "SELECT * FROM clima ORDER BY fecha DESC LIMIT 50"
        
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return False

        # Convertir fecha a objeto datetime para que Matplotlib la entienda
        df['fecha'] = pd.to_datetime(df['fecha'])

        # Crear la gráfica
        # 1. Crear la figura con 2 subplots (2 filas, 1 columna)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # --- PANEL SUPERIOR: TEMPERATURA ---
        ax1.plot(df['fecha'], df['temperatura'], color='tab:red', linewidth=2)
        ax1.set_ylabel('Temp (°C)', color='tab:red', fontsize=12)
        ax1.set_title('Histórico de Parámetros Ambientales', fontsize=14)
        ax1.grid(True, linestyle='--', alpha=0.6)

        # --- PANEL INFERIOR: PRESIÓN ---
        ax2.plot(df['fecha'], df['presion'], color='tab:blue', linewidth=2)
        ax2.set_ylabel('Presión (hPa)', color='tab:blue', fontsize=12)
        ax2.set_xlabel('Hora del Día', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.6)

        # 2. Formatear el eje del tiempo (X) para ambos
        xfmt = mdates.DateFormatter('%H:%M:%S')
        ax2.xaxis.set_major_formatter(xfmt)
        fig.autofmt_xdate() # Rota las fechas para que no se amontonen

        # 3. Ajustar espacio entre gráficas para que no se encimen los textos
        plt.tight_layout()

        # 4. Guardar
        plt.savefig('static/temp_ambiente.png')
        plt.close()
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False