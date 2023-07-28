from flask import Flask, render_template, request, redirect, url_for, flash
import flask
import jinja2
import pdfkit
import uuid
import os

app = flask.Flask(__name__)

RUTA_TEMPORAL = 'src/static/temp'

# Función para verificar si la extensión del archivo es permitida
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'gif'}

    # Obtener la extensión del archivo
    extension = filename.rsplit('.', 1)[1].lower()

    # Verificar si la extensión está permitida
    if '.' in filename and extension in extensiones_permitidas:
        print("yes")
        return True
    else:
        return False
    
# Función para obtener la extensión del archivo
def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

@app.route('/')
def home():
    return render_template('index.html')

# Generar pdf con datos optenidos de formulario    
@app.route('/generarPdf', methods=['GET', 'POST'])
def generarPdf():
    if request.method == 'POST':

        raza = request.form['raza']
        nombre_hermano = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['archivo']

        if(request.files['archivo'] and extensiones_validas(imagen.filename)):
            archivo_temporal = os.path.join(RUTA_TEMPORAL, str(uuid.uuid4()) + '.' + 'jpg')
            imagen.save(archivo_temporal)

            nombre_archivo = os.path.basename(archivo_temporal)
            imagen = 'E:/documentación etapa productiva -_-/Proyecto_APEI/GENERAR-PDF/Metodo con pdfkit/src/static/temp' + '/' + nombre_archivo

        else:
            return "archivo invalido como tu papa gonorrea"

        print(imagen)
        context = {'Raza': raza, 'imagen': imagen, 'descripcion': descripcion, 'nombre_hermano':nombre_hermano}

        template_loader = jinja2.FileSystemLoader('src/templates/plantillashtml')
        template_env = jinja2.Environment(loader=template_loader) 
        
        html_template = "plantilla1.html"
        template = template_env.get_template(html_template)
        output_text = template.render(context)

        # Configuración para pdfkit
        config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

        options = { 'page-size': 'Letter',
                    'margin-top': '0.05in',
                    'margin-right': '0.05in',
                    'margin-bottom': '0.05in',
                    'margin-left': '0.05in',
                    'encoding': 'UTF-8',
                    'disable-external-links': True,
                    'quiet': '',
                    'no-outline': None,
                    'print-media-type': None,
                    'load-error-handling': 'ignore',
                    'load-media-error-handling': 'ignore',
                    'load-error-handling': 'skip',
                    'enable-local-file-access': True}

        output_pdf = r"E:\documentación etapa productiva -_-\Proyecto_APEI\GENERAR-PDF\Metodo con pdfkit\src\static\pdf\pdf_generado.pdf"
        rutacss= r"E:\documentación etapa productiva -_-\Proyecto_APEI\GENERAR-PDF\Metodo con pdfkit\src\static\css\styleplantilla.css"

        pdfkit.from_string(output_text, output_pdf, css=rutacss, options = options, configuration=config)

        os.remove(archivo_temporal)

        # Devuelve una respuesta con el PDF adjunto para descargar
        return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True, port=3000)