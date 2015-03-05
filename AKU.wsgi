#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/AKU/")
activate_this = '/opt/virtual_env/AKU/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

