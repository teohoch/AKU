from wtforms.validators import ValidationError
import re


def validateJira(form, field):
	p = re.compile(ur'(^[a-zA-Z]+-\d+$)')
	if not re.search(p, field.data):
		raise ValidationError('Ticket Number MUST be in the format <letters>-<numbers>')


def validateIFP(form, field):
	if (field.data.filename != "IFP_Cal.xml"):
		raise ValidationError('File Name is Incorrect! Remeber that for IFProc, the filename MUST be IFP_Cal.xml')


def nameValidation(regex, regex_message, ste):
	fixed_message = regex_message
	message = 'File Name is Incorrect! Remeber that for {0}, the filename MUST be formated as {1}'.format(ste, fixed_message)

	def _name_validation(form, field):
		p = re.compile(regex)
		if not re.search(p, field.data.filename):
			raise ValidationError(message)

	return _name_validation