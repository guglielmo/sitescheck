import os
import sys
import site

PROJECT_ROOT = '/home'
site_packages = '/root/.virtualenvs/sitescheck/lib/python2.5/site-packages')
site.addsitedir(os.path.abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'sitescheck.settings_staging'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
