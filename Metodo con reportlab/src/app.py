from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import uuid
import os

app = Flask(__name__)

# ruta especificada
RUTA_PDF = 'src/static/pdf'
# Ruta temporal para almacenar los archivos cargados
RUTA_TEMPORAL = 'src/static/temp'

@app.route('/')
def home():
    return render_template('index.html')
        

@app.route('/generar_pdf', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        # Procesa los datos enviados por el formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        archivo = request.files['archivo']  

        # Ruta completa del archivo PDF
        pdf_filename = os.path.join(RUTA_PDF, 'formulario.pdf')

        # Guardar el archivo temporalmente en el servidor
        archivo_temporal = os.path.join(RUTA_TEMPORAL, str(uuid.uuid4()) + '.png')
        archivo.save(archivo_temporal)

        # Generar el PDF utilizando ReportLab
        c = canvas.Canvas(pdf_filename, pagesize=A4)

        # Para títulos asignamos una fuente y el tamaño = 20
        c.setFont('Helvetica', 20)
        # Dibujamos el título con el texto proporcionado en el formulario
        c.drawString(25, 800, nombre)

        # Para párrafos normales cambiamos el tamaño a 12
        c.setFont('Helvetica', 12)
        # Dibujamos el párrafo con el texto proporcionado en el formulario
        c.drawString(25, 780, descripcion)
        # c.drawString(100, 650, "Este es otro texto largo que se ajusta al ancho máximo.", maxWidth=150)

        try:
            # Intenta cargar la imagen desde la ruta temporal
            c.drawImage(archivo_temporal, 25, 480, 480, 270)
        except OSError as e:
            # Si hay un error al cargar la imagen, muestra el mensaje y continúa sin la imagen
            print(f"Error al cargar la imagen: {e}")

        # Cerrar el PDF
        c.save()

        # Eliminar el archivo temporal
        os.remove(archivo_temporal)

        # Redirige al usuario a la nueva ruta para descargar el PDF
        return redirect(url_for('descargar_pdf'))


@app.route('/descargar-pdf')
def descargar_pdf():
    # Ruta completa del archivo PDF
    pdf_filename = os.path.join('static/pdf/formulario.pdf')
    
    # Devuelve el PDF al usuario para que pueda descargarlo.
    return send_file(
        pdf_filename,
        as_attachment=False,
        mimetype='application/pdf'
    )


if __name__ == '__main__':
    os.makedirs(RUTA_PDF, exist_ok=True)
    os.makedirs(RUTA_TEMPORAL, exist_ok=True)
    app.run(debug=True, port=3000)