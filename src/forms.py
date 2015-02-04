from wtforms import StringField, IntegerField, PasswordField, SelectField, HiddenField, SubmitField, validators
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from customValidators import *

#DEVICES = [('IFProc', 'IFProc'),('ColdCart3', 'ColdCart3'),('WCA3', 'WCA3')]

#STES = [('AOS', 'AOS'), ('TFINT', 'TFINT'), ('TFSD', 'TFSD'), ('TFOHG', 'TFOHG'), ('TFENG', 'TFENG'), ('FE-LAB', 'FE-LAB'), ('BE-LAB', 'BE-LAB')]




class LoginForm(Form):
	username = StringField('Username', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])
	submit_button = SubmitField('Log In')


class TicketForm(Form):
	Device = SelectField('Select the corresponding device:', validators=[validators.DataRequired()])
	STE = SelectField('Select the corresponding STE:', validators=[validators.DataRequired()])
	Ticket = StringField('Introduce the ticket number: ', validators=[validateJira])
	submit_button = SubmitField('Submit')


class UploadForm(Form):
	conf = FileField('Select Configuration File ', validators=[FileRequired()])
	submit_button = SubmitField('Upload')

class IfpUploadForm(Form):
	conf = FileField('Select Configuration File ', validators=[FileRequired(), validateIFP])
	Serial = IntegerField('Introduce the corresponding Serial for IFProc:',validators=[validators.DataRequired()])
	submit_button = SubmitField('Upload')

