from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include(admin.site.urls)),
    (r'^diff/(?P<content_id>\d+)$', 'sitescheck.views.diff'),  
)

# static media (not for production!)
if (settings.ENVIRONMENT != 'production'):
  urlpatterns += patterns('',
    (r'^robots.txt$', 'django.views.static.serve', 
      { 'path' : "/robots.txt", 
        'document_root': settings.TEMPLATE_DIRS[0],
        'show_indexes': False } ),
    (r'^favicon.ico$', 'django.views.static.serve', 
      { 'path' : "/favicon.ico", 
        'document_root': settings.TEMPLATE_DIRS[0],
        'show_indexes': False } ),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': "%s/css" % settings.TEMPLATE_DIRS[0]}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': "%s/images" % settings.TEMPLATE_DIRS[0]}),
    (r'^fonts/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': "%s/fonts" % settings.TEMPLATE_DIRS[0]}),
    (r'^javascripts/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': "%s/javascripts" % settings.TEMPLATE_DIRS[0]}),  
  )
