from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    message = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Enviar')