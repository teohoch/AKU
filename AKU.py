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

		form.Device.choices = select_field_transform(devices)
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
		well_formed = xml_well_formed(os.path.join(app.config['UPLOAD_FOLDER'], session['filename']))
		if not session['device']=='IFProc' and well_formed:
			corresponds = correspond_to_device(os.path.join(app.config['UPLOAD_FOLDER'], session['filename']), session['device'])
			scheme_valid = validate_scheme(os.path.join(app.config['UPLOAD_FOLDER'], session['filename']), session['device'])
			#if 'Coldcart' in session['device'] or 'WCA' in session['device']:


		if (well_formed and corresponds and scheme_valid):
			return 'You did it >:D!'
		return 'Cuek'



if __name__ == '__main__':
	app.run()