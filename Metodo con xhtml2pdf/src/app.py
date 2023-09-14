
# Apartado donde se importaran todos los modulos necesarios para el funcionamiento del proyecto.
from flask import Flask, render_template, Response, request
from tempfile import TemporaryFile
import io
from xhtml2pdf import pisa

# Variable que guarda el nombre del archivo de arranque para la ejecución del codigo. 
app = Flask(__name__)

# Ruta principal donde se encuentra el formulario para la generación de pdf.
@app.route('/')
def home():
    return render_template("index.html")

# Función para verificar si la extensión del archivo es compalible.
def extensiones_validas(filename):
    # Lista de extensiones permitidas para los archivos de imagen.
    extensiones_permitidas = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Obtener la extensión del archivo.
    extension = filename.rsplit('.', 1)[1].lower()

    # Verificar si la extensión está permitida.
    if '.' in filename and extension in extensiones_permitidas:
        return True
    else:
        return False

@app.route('/generar_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        # Captura los datos del formulario
        raza = request.form['raza']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['archivo']

        # Condicional donde utilizaremos la funcion de extensiones_validas, para evaluar si el archivo esta permitido o no.
        if(request.files['archivo'] and extensiones_validas(imagen.filename)):
            # Crea un archivo temporal para guardar la imagen
            with TemporaryFile(delete=False) as tmp_file:
                imagen.save(tmp_file)

            # Obtén la ruta del archivo temporal
            ruta_temporal = tmp_file.name
        else:
            # En caso de no tener un archivo permitido se retornara el mensaje de error.
            return "archivo invalido"         
           
        # Renderiza la plantilla HTML y reemplaza los marcadores de posición con datos
        rendered_template = render_template('example.html', raza=raza, nombre_hermano=nombre, descripcion=descripcion, imagen=ruta_temporal)
        
        # Combina el contenido HTML y los estilos CSS
        css_file = open('E:/documentación etapa productiva -_-/Proyecto_APEI/GENERAR-PDF/Metodo con xhtml2pdf/src/static/css/style.css', 'r').read()
        html_content = f"{rendered_template}\n<style>{css_file}</style>"
        
        # Crea un objeto de tipo BytesIO para almacenar el PDF generado
        pdf_buffer = io.BytesIO()
        
        # Genera el PDF a partir del contenido HTML con estilos CSS
        pisa.CreatePDF(src=html_content, dest=pdf_buffer)
        
        # Mueve el puntero al inicio del objeto BytesIO
        pdf_buffer.seek(0)
        
        # Crea un objeto Response para enviar el PDF al navegador
        response = Response(pdf_buffer.read(), content_type='application/pdf')
        
        # Agrega el encabezado para la descarga del PDF
        response.headers['Content-Disposition'] = 'inline; filename=mi_pdf.pdf'
        
        # Ruta completa de guardado (puedes cambiarla según tus necesidades)
        ruta_de_guardado = 'E:/documentación etapa productiva -_-/Proyecto_APEI/GENERAR-PDF/Metodo con xhtml2pdf/src/static/pdf/pdfgenerado.pdf'

        # Guarda el archivo PDF con el nombre generado automáticamente
        with open(ruta_de_guardado, 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.getvalue())
        
        return response
    else:
        # Si no se envió el formulario, muestra un mensaje
        mensaje = "No se encontraron datos, por lo que no es posible generar el PDF correctamente."
        return mensaje


if __name__ == '__main__':
    app.run(debug=True,  port=5030)