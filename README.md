## Generar-pdf-flask
In the present repository it is empirically illustrated how to generate pdf files through data sent through an html form using flask and reportlab

## Requisitos previos
* Python [python download](https://www.python.org/downloads/release/python-31010/)
---

```sh
# Otorgar permisos a windows en caso de ser solicitados
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process    
```
```sh
# Crear entorno virtual
virtualenv env   
```
```sh
# Activar entorno virtual para instalar dependencias
env/Scripts/activate 
```
```sh
# Instalar las dependencias que necesitaremos en este proyecto
pip install -U -r requirements.txt
```
```sh
# Para correr el proyecto
python src/app.py 
```
