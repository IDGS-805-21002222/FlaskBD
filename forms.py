from wtforms import Form
from flask_wtf import FlaskForm
 
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
 
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms import validators

class UserForm2(FlaskForm):  # Cambia 'Form' por 'FlaskForm'
    id = IntegerField('id', [
        validators.NumberRange(min=1, max=20, message='Valor no válido')
    ])
    
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El nombre es requerido'),
        validators.Length(min=4, max=20, message='Requiere min=4 max=20')
    ])
   
    apaterno = StringField('Apellido Paterno', [
        validators.DataRequired(message='El apellido es requerido')
    ])
   
    email = EmailField('Correo', [
        validators.DataRequired(message='El correo es requerido'),
        validators.Email(message='Ingrese un correo válido')
    ])
