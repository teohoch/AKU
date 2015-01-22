import ConfigParser
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
CONFIGURATION_PATH = '/home/teohoch/PycharmProjects/AKU/Configuration/conf.ini'

config = ConfigParser.ConfigParser()
config.read(CONFIGURATION_PATH)
UPLOAD_FOLDER = config.get('Locations', 'Uploads')


