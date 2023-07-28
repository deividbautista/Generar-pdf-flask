# Apartado para importar todos los modulos necessarios.
from flask import Flask, render_template, request, redirect, url_for, flash
import flask
import jinja2
import pdfkit
import uuid
import os

# Definimos variable app para inicializar el servidor.
app = flask.Flask(__name__)

# ---------------------------------------------------------------------------
# Apartado de rutas importantes.
RUTA_TEMPORAL = 'src/static/temp'
output_pdf = r"E:\documentación etapa productiva -_-\Proyecto_APEI\GENERAR-PDF\Metodo con pdfkit\src\static\pdf\pdf_generado.pdf"
rutacss= r"E:\documentación etapa productiva -_-\Proyecto_APEI\GENERAR-PDF\Metodo con pdfkit\src\static\css\stylePlantilla.css"
# ---------------------------------------------------------------------------


# Función para verificar si la extensión del archivo es compalible.
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen.
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'gif'}

    # Obtener la extensión del archivo.
    extension = filename.rsplit('.', 1)[1].lower()

    # Verificar si la extensión está permitida.
    if '.' in filename and extension in extensiones_permitidas:
        print("yes")
        return True
    else:
        return False
    
# -------------------------------------------------------------------------
# Seccion de ruta principal
# -------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -------------------------------------------------------------------------
# Seccion de generación de pdf
# -------------------------------------------------------------------------  
@app.route('/generarPdf', methods=['GET', 'POST'])
# Función general para generar pdf.
def generarPdf():
    # Condicional para corroborar la recepción de los datos en el formulario.
    if request.method == 'POST':
        
        # Datos obtenidos del formulario.
        raza = request.form['raza']
        nombre_hermano = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['archivo']

        # Condicional donde utilizaremos la funcion de extensiones_validas, para evaluar si el archivo esta permitido o no.
        if(request.files['archivo'] and extensiones_validas(imagen.filename)):
            archivo_temporal = os.path.join(RUTA_TEMPORAL, str(uuid.uuid4()) + '.' + 'jpg')
            imagen.save(archivo_temporal)

            # Aqui obtenemos el nombre del archivo que estamos reicibiendo del formulario.
            nombre_archivo = os.path.basename(archivo_temporal)
            # Definimos el valor de imagen para obtener la ruta absoluta en donde se esta guardando el archivo de manera temporal.
            imagen = 'E:/documentación etapa productiva -_-/Proyecto_APEI/GENERAR-PDF/Metodo con pdfkit/src/static/temp' + '/' + nombre_archivo
        else:
            # En caso de no tener un archivo permitido se retornara el mensaje de error.
            return "archivo invalido como tu papa gonorrea"

        # Definimos la variable context para definir los apartados a renderizar en la plantilla html antes de construir el pdf.
        context = {'Raza': raza, 'imagen': imagen, 'descripcion': descripcion, 'nombre_hermano':nombre_hermano}

        template_loader = jinja2.FileSystemLoader('src/templates/plantillashtml')
        # Definimos la variable que guarde la ruta de la plantilla html
        template_env = jinja2.Environment(loader=template_loader) 
        # Definimos la variable que almacenara nuestra plantilla html
        html_template = "plantilla1.html"
        template = template_env.get_template(html_template)
        # Definimos la variable donde se guarda el renderizado de la plantilla con los valores definidos en context
        output_text = template.render(context)

        # Configuración para pdfkit con el archivo externo wkhtmltopdf.
        config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

        # Definimos las opciones sobre configuración que vamos aplicar a la hora de construir el pdf, que posee las caracteristicas del archivo. 
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

        # Finalmente construimos el pdf con las caracteristicas anteriormente definidas.
        pdfkit.from_string(output_text, output_pdf, css=rutacss, options = options, configuration=config)

        # Removemos el archivo temporal.
        os.remove(archivo_temporal)

        # Devuelve una respuesta con el PDF adjunto para descargar.
        typeAlert = 1
        return render_template('index.html', typeAlert=typeAlert)

if __name__ == '__main__':
    app.run(debug=True, port=3000)