from flask import Flask, render_template, request
import os
import sys
from flask import send_file
from reporte import exportar_pdf

app = Flask(__name__)

@app.route('/descargar')
def descargar():
    fecha_reporte = request.args.get('fecha') 
    path_img = 'static/temp_reporte.png'
    # Generamos el PDF usando la imagen que ya está en pantalla
    path_pdf = exportar_pdf(path_img, fecha_reporte )
    return send_file(path_pdf, as_attachment=True)
# Añadimos la carpeta superior al sistema de búsqueda de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from graficar import generar_grafica



# Ruta principal: Lo que verás al entrar a la IP de tu Raspberry
@app.route('/', methods=['GET', 'POST'])
def index():
    imagen = None
    if request.method == 'POST':
    #DATOS QUE ESCRIBA EL USUARIO
        dia = request.form.get('dia')
        inicio = request.form.get('inicio')
        fin = request.form.get('fin')

        #LLAMAR FUNCIÓN QUE GENERA LA GRÁFICA
        imagen = generar_grafica(dia, inicio, fin)
    return render_template('index.html', imagen=imagen)

if __name__ == '__main__':
    # '0.0.0.0' permite que otros dispositivos en tu red local vean la web
    app.run(debug=True, host='0.0.0.0', port=5000)