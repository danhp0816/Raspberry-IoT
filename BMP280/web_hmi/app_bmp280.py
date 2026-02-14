from flask import Flask, render_template, request
from graf_bmp280 import generar_reporte_ambiental
from graf_cpu import generar_reporte_cpu

app = Flask(__name__)
DB_AMB = '/home/rpi5-dev/Scripts/BMP280/ambiente.db'
DB_CPU = '/home/rpi5-dev/Scripts/sensores.db'

@app.route('/', methods=['GET', 'POST'])
def index():
    hay_amb=False
    hay_cpu=False
    dia = request.form.get('dia')
    inicio = request.form.get('inicio', '00:00:00')
    fin = request.form.get('fin', '23:59:59')
    
    # Generamos las dos gráficas al mismo tiempo
    # Pasamos los mismos parámetros de tiempo a ambas funciones
    if request.method == 'POST':

        hay_amb = generar_reporte_ambiental(DB_AMB, dia, inicio, fin)
        hay_cpu = generar_reporte_cpu(DB_CPU, dia, inicio, fin) 

    return render_template('index.html', 
                           hay_amb=hay_amb, 
                           hay_cpu=hay_cpu, 
                           dia=dia, inicio=inicio, fin=fin)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 

