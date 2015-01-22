from wtforms import StringField, IntegerField, PasswordField, SelectField, HiddenField, validators
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from customValidators import *

#DEVICES = [('IFProc', 'IFProc'),('ColdCart3', 'ColdCart3'),('WCA3', 'WCA3')]

#STES = [('AOS', 'AOS'), ('TFINT', 'TFINT'), ('TFSD', 'TFSD'), ('TFOHG', 'TFOHG'), ('TFENG', 'TFENG'), ('FE-LAB', 'FE-LAB'), ('BE-LAB', 'BE-LAB')]


def select_field_transform(data):
	fixed = []
	for k in data:
		d = str(k[0])
		fixed.append([d,d])
	return fixed

class LoginForm(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])


class TicketForm(Form):
	Device = SelectField('Select the corresponding device:', validators=[validators.DataRequired()])
	STE = SelectField('Select the corresponding STE:', validators=[validators.DataRequired()])
	Ticket = StringField('Introduce the ticket number: ', validators=[validateJira])


class UploadForm(Form):
	conf = FileField('Select Configuration File ', validators=[FileRequired()])

class IfpUploadForm(Form):
	conf = FileField('Select Configuration File ', validators=[FileRequired(), validateIFP])
	Serial = IntegerField('Introduce the corresponding Serial for IFProc:',validators=[validators.DataRequired()])