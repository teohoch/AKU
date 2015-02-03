import ConfigParser
import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
CONFIGURATION_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Configuration/conf.ini'))

config = ConfigParser.ConfigParser()
config.read(CONFIGURATION_PATH)
UPLOAD_FOLDER = config.get('Locations', 'Uploads')



