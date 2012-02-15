import os
import sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)

sys.path.append(workspace)

sys.path.append('/Users/haak/M2M/lib/python2.7/site-packages')
sys.path.append('/Users/haak/M2M/SiteCode/m2m')


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
