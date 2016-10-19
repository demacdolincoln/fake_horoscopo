from flask_wtf import Form
from wtforms import SelectField, TextAreaField, SubmitField, TextField
from wtforms import  PasswordField, RadioField, SelectMultipleField
from wtforms.validators import Required, Length
from database import *

class Signo_form(Form):
    _choices = [('aries', 'Áries'),
	     ('taurus', 'Touro'),
	     ('gemini', 'Gêmeos'),
	     ('cancer', 'Câncer'),
	     ('leo', 'Leão'),
	     ('virgo', 'Virgem'),
	     ('libra', 'Libra'),
	     ('scorpion', 'Escorpião'),
	     ('sagittarius', 'Sagitário'),
	     ('capricorn', 'Capricórnio'),
	     ('aquarius', 'Aquário'),
	     ('pisces', 'Peixes')]
    signos = SelectField("Signos", choices=_choices, validators=[Required()])
    submit = SubmitField("Consultar")

class Send_message(Form):
	mensagem = TextAreaField("Digite a mensagem...", 
                                validators=[Required(), Length(min=10,max=200)])
	submit = SubmitField("Enviar")

class Login_form(Form):
	name = TextField("name", validators=[Required()])
	passwd = PasswordField("passwd", validators=[Required()])
	submit = SubmitField("login")


class Action_mod(Form):
	_data = data_sql().get_all_texts()
	texts = SelectMultipleField("Frases", choices=_data)
	exe = RadioField("actions", choices=[("accept","accept"), ("recuse","recuse")])
	submit = SubmitField("executar")