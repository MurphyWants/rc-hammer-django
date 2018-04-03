"""
WSGI config for rc_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rc_server.settings")

application = get_wsgi_application()

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
'''
https://stackoverflow.com/questions/36210686/importerror-no-module-named-mysite-settings-django/36211423

Daphne gets error: ImportError: No module named 'rc_car.settings'

'''
