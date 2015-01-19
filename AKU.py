from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from forms import *
from xmlverification import *
from database import Aku_Database



app = Flask(__name__)
app.config.from_object('config')
app.debug = True

db = Aku_Database(app.config['DB_PATH'])
ste = db.get_all_ste()
devices = db.get_all_devices()

@app.route('/')
def index():
	return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	return render_template('login.html', form=form)

@app.route('/aku/')
def akuDefault():
	return redirect('/aku/1/')

def loader(form):
	if form.validate_on_submit():
		if form.conf:
			filename = secure_filename(form.conf.data.filename)
			form.conf.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			session['filename'] = filename
		if session['device'] == 'IFProc':
			session['serial'] == form.Serial.data
		return redirect('/aku/3/')
	return render_template('upload.html',form=form)

@app.route('/aku/<int:number>/', methods=['GET', 'POST'])
def aku(number):
	if number == 1:
		form = TicketForm()

		form.Device.choices = devices
		form.STE.choices = select_field_transform(ste)

		if form.validate_on_submit():
			session['device'] = form.Device.data
			session['ste'] = form.STE.data
			session['ticket'] = form.Ticket.data
			return redirect('/aku/2/')
		return render_template('ticket.html', form=form)
	elif number == 2:
		if session['device'] == 'IFProc':
			form = IfpUploadForm()
			return loader(form)

		else:
			form = UploadForm()
			return loader(form)
		form = UploadForm()
		return render_template('upload.html', form=form)
	elif number == 3:
		return render_template('review.html')
	elif number == 4:
		filename = os.path.join(app.config['UPLOAD_FOLDER'], session['filename'])
		checks = []
		checks.append(xml_well_formed(filename))
		if not session['device']=='IFProc' and checks[0][0]:

			device_name = db.get_device_from_value(session['device'])[0][0]

			checks.append(correspond_to_device(filename, device_name))
			checks.append(validate_scheme(filename, device_name))

			if 'ColdCart' in device_name or 'WCA' in device_name:
				checks.append(freq_order_file_check(filename))
				if 'ColdCart' in device_name:
					checks.append(polarization_angle_check(filename))

		status = True

		for item in checks:
			status = status and item[0]

		return render_template('xmlanalysis.html',analicis_status=checks, status=status)







if __name__ == '__main__':
	app.run()