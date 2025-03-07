import secrets  # <-- Asegúrate de que esta línea esté al inicio

from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig

from models import db
from models import Alumnos

import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.secret_key = secrets.token_hex(16)  # Genera una clave segura única

csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.route("/",methods=['GET','POST'])
@app.route("/index")
def index():
    create_form=forms.UserForm2(request.form)
    
    alumno=Alumnos.query.all()
    
    return render_template("index.html", form=create_form,alumnos=alumno)

@app.route("/detalles",methods=['GET','POST'])
def detalles():
    create_form=forms.UserForm2(request.form)
    if request.method == 'GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        nom=alum1.nombre
        ape=alum1.apellido
        email=alum1.email        
    return render_template("detalles.html", form=create_form,nombre=nom, apellido=ape, email=email)

@app.route("/Alumnos1",methods=['GET','POST'])
def Alumnos1():
    create_form=forms.UserForm2(request.form)
    if request.method == 'POST':
        alum=Alumnos(
            create_form.nombre.data,
            create_form.apaterno.data,
            create_form.email.data)
        #insert alumnos() values()
        db.session.add(alum)       
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos1.html", form=create_form)


@app.route('/modificar', methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')

        if id is None:
            flash("ID no proporcionado", "danger")
            return redirect(url_for('index'))

        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alum1 is None:
            flash("Alumno no encontrado", "danger")
            return redirect(url_for('index'))

        create_form.id.data = id
        create_form.nombre.data = alum1.nombre.strip()
        create_form.apaterno.data = alum1.apellido  # Corrige si tu modelo usa 'apellido' en lugar de 'apaterno'
        create_form.email.data = alum1.email

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alum1:
            alum1.nombre = create_form.nombre.data.strip()
            alum1.apellido = create_form.apaterno.data  # Usa 'apellido' si tu modelo lo tiene así
            alum1.email = create_form.email.data

            db.session.commit()
            flash("Alumno modificado con éxito", "success")
            return redirect(url_for('index'))

        flash("Error al modificar el alumno", "danger")

    return render_template("modificar.html", form=create_form)



@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm2(request.form)
    
    id = request.args.get('id')  # Obtener el ID desde los parámetros de la URL
    
    if id is None:
        flash("ID no proporcionado", "error")
        return redirect(url_for('index'))
    
    alum = Alumnos.query.get(id)  # Buscar al alumno por ID
    
    if not alum:
        flash("Alumno no encontrado", "error")
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        # Llenar el formulario con los datos del alumno encontrado
        create_form.id.data = alum.id
        create_form.nombre.data = alum.nombre
        create_form.apaterno.data = alum.apellido  # Ajustado a "apellido" en vez de "apaterno"
        create_form.email.data = alum.email

    if request.method == 'POST':
        db.session.delete(alum)  # Eliminar el alumno
        db.session.commit()
        flash("Alumno eliminado correctamente", "success")
        return redirect(url_for('index'))

    return render_template("eliminar.html", form=create_form)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)