import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import argparse
from datetime import datetime

def generar_grafica(fecha_filtro, hora_inicio, hora_fin):
    # 1. Conectar y extraer datos
    DB_PATH = '/home/rpi5-dev/Scripts/sensores.db'
    conexion = sqlite3.connect(DB_PATH)
    query = f"""
    SELECT fecha, temperatura
    FROM lecturas
    WHERE fecha >= '{fecha_filtro} {hora_inicio}'
        AND fecha <= '{fecha_filtro} {hora_fin}'
    ORDER BY fecha ASC
    """
    df = pd.read_sql_query(query,conexion)
    conexion.close()
    
    if df.empty:
        print(f"⚠️ No hay datos para el rango: {fecha_filtro} de {hora_inicio} a {hora_fin}")
        return
    
    # Convertir la columna de fecha a formato tiempo real
    df['fecha'] = pd.to_datetime(df['fecha'])
    if df['temperatura'].dtype == 'object':
        df['temperatura']=df['temperatura'].str.replace('=','').astype(float)
    else:
        df['temperatura'].astype(float)
    df = df.sort_values('fecha')
    
    # 1. Calcular los valores clave
    max_temp =float(df['temperatura'].max())
    min_temp =float(df['temperatura'].min())

    # 3. Gráfica Profesional
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['fecha'], df['temperatura'], marker='.', linestyle='-', color='#FF8C00', linewidth=1, label='Temp CPU')

    # 4. Formatear el eje del Tiempo (cada 10 minutos por ejemplo)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=10))

    # 5. Agregar cuadrícula y límites claros
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_ylabel('Temperatura (°C)', fontweight='bold')
    ax.set_xlabel('Hora del día', fontweight='bold')
    ax.set_title(f'Monitoreo Térmico Raspberry Pi 5 \n{fecha_filtro}', fontsize=14, pad=20)
    ax.legend()

    # 1. Configurar el eje Y (Temperatura)
    # Ponemos una marca cada 2 grados (puedes cambiarlo a 5 si prefieres)
    ax.yaxis.set_major_locator(MultipleLocator(2)) 

    # 2. Opcional: Agregar marcas menores (ticks pequeños) cada 0.5 grados
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    # 3. Ajustar los límites para que no se vea apretado
    # Le damos 2 grados de margen arriba del máximo y abajo del mínimo
    ax.set_ylim(min_temp - 2, max_temp + 2)

    # 4. Reforzar la cuadrícula para que siga estas nuevas marcas
    ax.grid(True, which='major', linestyle='-', alpha=0.6)
    ax.grid(True, which='minor', linestyle=':', alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'reporte_{fecha_filtro}_{hora_inicio}h.png')
    print("Gráfica generada con éxito")

    path_imagen = 'static/temp_reporte.png'
    plt.savefig(path_imagen)
    plt.close()
    return path_imagen

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='Graficador de Temperatura con Filtros')
    parser.add_argument('--dia', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='Fecha en formato YYYY-MM-DD')
    parser.add_argument('--inicio', type=str, default='00:00:00', help='Hora inicio HH:MM:SS')
    parser.add_argument('--fin', type=str, default='23:59:59', help='Hora fin HH:MM:SS')
    
    args = parser.parse_args()
    generar_grafica(args.dia, args.inicio, args.fin)   