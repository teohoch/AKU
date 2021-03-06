import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask.ext.login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap

from forms import *
from xmlverification import XmlVerification
from database import Aku_Database
from svncontrols import AkuSvn
from sshconnection import ssh_command
from ldapconnection import validateLDAP as ld
from helpers import *
import config

# Delete this one
from time import sleep


app = Flask(__name__)

app.config.from_object(config)
app.debug = True
app.jinja_env.autoescape = True

Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = Aku_Database(app.config['CONFIGURATION_PATH'])
ste = db.get_all_ste()
devices = db.get_all_devices()


class User(UserMixin):
	def __init__(self, uid=None, name=None, passwd=None):

		self.active = False

		ldapres = ld(uid=uid, username=name, password=passwd)

		if ldapres is not None:
			self.name = ldapres['name']
			self.username = ldapres['username']
			self.id = ldapres['id']

			# assume that a disabled user belongs to group 404
			if ldapres['gid'] != 404:
				self.active = True
			self.active = True

			self.gid = ldapres['gid']

	def is_active(self):
		return self.active

	def get_id(self):
		return self.id


@login_manager.user_loader
def load_user(userid):
	return User(uid=userid)


@app.route('/history/')
def index():
	uploads = db.get_n_uploads(15)
	return render_template('Index.html', home=True, uploads=uploads, ste_dic=to_dictionary(ste),
	                       device_dic=to_dictionary(db.get_all_devices_with_id()))


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(name=form.username.data, passwd=form.password.data)
		if user.active is not False:
			login_user(user)
			flash("Logged in successfully.")
			return redirect('/')
		else:
			flash("Your username/password is wrong")
	return render_template("login.html", form=form)


@app.route('/favicon.ico/')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
	logout_user()
	flash("You've been successfully Logged Out")
	return redirect('/')


@login_manager.unauthorized_handler
def unauthorized():
	flash('You must first be Logged In to access this feature!')
	return redirect('/login')


def loader(form):
	print(form.validate_on_submit())
	if form.validate_on_submit() and form.conf:
	# ## Get and check Device!! ###

		session['ste'] = form.STE.data
		session['ticket'] = form.Ticket.data

		filename = secure_filename(form.conf.data.filename)
		form.conf.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		session['filename'] = filename

		check = XmlVerification(app.config['CONFIGURATION_PATH'], os.path.join(app.config['UPLOAD_FOLDER'], filename), name=filename)
		check_d = check.check_correct_device()
		dev = check.get_device_from_xml()
		if check_d[0]:
			session['device'] = check.get_device_from_xml()
			if not session['device'] == 'IFProc':
				session['serial'] = None
			return redirect('/aku/2/')
		else:
			flash("You are trying to upload a configuration file for "+ dev + ". The correct Filename format is " + check_d[1])
			return render_template('ticket.html', upload=True, form=form)
	return render_template('ticket.html', upload=True, form=form)


def favicon():
	return url_for('.static', filename='favicon.ico')


@app.route('/update/')
def enforce_update():
	return str(ssh_command('AOS', app.config['CONFIGURATION_PATH'], 'ls'))


@app.route('/')
@app.route('/aku/')
@app.route('/aku/<int:number>/', methods=['GET', 'POST'])
@login_required
def aku(number=1):
	if number == 1:
		form = TicketForm()
		form.STE.choices = select_field_transform(ste)
		return loader(form)
	elif number == 2:
		form = SerialForm()
		if not form.validate_on_submit():
			if session['device'] == 'IFProc':
				return render_template('serialstop.html',form=form, upload=True)
			else:
				return render_template('pitstop.html', upload=True)
		else:
			session['serial'] = form.Serial.data
			return render_template('pitstop.html', upload=True)
	elif number ==3:
		sleep(5)
		return 'whiii'
	elif number == 4:
		form = Form()
		force = False
		if request.method == 'POST':
			force = (request.form['btn'] == 'Confirm Upload')

			if (request.form['btn'] == 'Cancel'):
				to_clear = ['filename', 'device', 'ste', 'ticket']
				if session['device'] == 'IFProc':
					to_clear.append('serial')
				for key in to_clear:
					session[key] = ''
				return redirect('/')
			if (request.form['btn'] == 'Retry'):
				return redirect('/aku/')

		filename = os.path.join(app.config['UPLOAD_FOLDER'], session['filename'])
		file_processed = session['filename']
		device_name = db.get_device_from_value(session['device'])[0][0]

		test = XmlVerification(app.config['CONFIGURATION_PATH'], filename, session['filename'])

		checks = [test.xml_well_formed()]
		if checks[0][0]:
			if not session['device'] == 'IFProc':

				checks.append(test.correspond_to_device())
				checks.append(test.validate_scheme())

				if 'ColdCart' in device_name or 'WCA' in device_name:
					checks.append(test.freq_order_file_check())
					if 'ColdCart' in device_name:
						checks.append(test.polarization_angle_check())
			else:
				checks.append(test.ifpProcessing(session['serial']))
				file_processed = "ifp_%d.xml" % session['serial']

		status = True
		svn_status = []
		db_status = False
		ssh_status = False

		for item in checks:
			status = status and item[0]

		if status:
			svn = AkuSvn(app.config['CONFIGURATION_PATH'])
			svn_status = svn.uploadToRepo(app.config['UPLOAD_FOLDER'], file_processed, current_user.username, force, session['ticket'])

			if svn_status[1] and (svn_status[0] or force):
				data = {
					'ste': session['ste'],
					'device': device_name,
					'ticket': session['ticket'],
					'filename': file_processed,
					'action': svn_status[0],
					'serial': session['serial'],
					'username': current_user.username}
				db_status = db.add_upload(data)

				ssh_status = ssh_command(session['ste'], app.config['CONFIGURATION_PATH'], 'updateAssemblies')

		uploaded = status and svn_status[1]
		registered = uploaded and db_status
		updated = registered and ssh_status

		completed = [uploaded, registered, updated]

		return render_template('xmlanalysis.html', upload=True, analicis_status=checks, status=status, svnstatus=svn_status,
		                       filename=file_processed, db_status=db_status, ssh_status=ssh_status, ste=session['ste'],
		                       force=force, form=form, completed=completed)





if __name__ == '__main__':
	app.run('0.0.0.0')