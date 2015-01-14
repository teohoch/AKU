from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SelectField,   validators
from flask_wtf import Form
from flask_wtf.file import FileField,FileRequired,FileAllowed



STES=[('AOS', 'AOS'), ('TFINT', 'TFINT'), ('TFSD', 'TFSD'), ('TFOHG', 'TFOHG'), ('TFENG', 'TFENG'), ('FE-LAB', 'FE-LAB'), ('BE-LAB', 'BE-LAB')]


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class UploadForm(Form):
    ste = SelectField('Select the corresponding STE', choices=STES)
    conf = FileField('Select Configuration File ', validators=[FileRequired()])


app = Flask(__name__)
app.config.from_object('config')
app.debug = True

@app.route('/')
def index():
    return 'Index Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    #if request.method == 'POST' and form.validate():
     #   user = User(form.username.data, form.email.data,
      #              form.password.data)
       # db_session.add(user)
        #flash('Thanks for registering')
        #return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.conf
        if file:
            filename = secure_filename(file.data.filename)
            file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploadsuccess', filename=filename))

    return render_template('upload.html', form=form)

@app.route('/uploadsuccess/<filename>', methods=['GET'])
def uploadsuccess(filename):
    return render_template('uploadsuccess.html',filename=filename)

if __name__ == '__main__':
    app.run()