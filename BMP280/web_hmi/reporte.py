from fpdf import FPDF
from datetime import datetime
import os

def exportar_pdf(path_grafica, dia):
    pdf = FPDF()
    pdf.add_page()
    
    # Título Principal
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SISTEMA DE MONITOREO TÉRMICO - RPi5", ln=True, align='C')
    
    # Metadatos del Reporte
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Fecha de consulta: {dia}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Reporte generado el: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='L')
    pdf.ln(10)
    
    # Insertar la Gráfica
    if os.path.exists(path_grafica):
        pdf.image(path_grafica, x=10, y=50, w=190)
    else:
        pdf.cell(200, 10, txt="Error: Imagen no encontrada", ln=True, align='C')
    
    # Pie de página técnico
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, txt="Este documento es un reporte automático generado por el sistema de instrumentación.", align='C')
    
    output_path = "static/reporte_final.pdf"
    pdf.output(output_path)
    return output_path