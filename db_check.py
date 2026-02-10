import sqlite3

try:
    conn = sqlite3.connect('/home/rpi5-dev/Scripts/sensores.db')
    cursor = conn.cursor()
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM lecturas")
    total = cursor.fetchone()[0]
    
    # Obtener el último
    cursor.execute("SELECT * FROM lecturas ORDER BY id DESC LIMIT 1")
    ultimo = cursor.fetchone()
    
    print(f"--- Resumen de Base de Datos ---")
    print(f"Total de registros: {total}")
    print(f"Última lectura: {ultimo}")
    
except sqlite3.Error as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()