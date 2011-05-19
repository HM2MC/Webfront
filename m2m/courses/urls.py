from django.conf.urls.defaults import *


urlpatterns = patterns('courses.views',
	(r'^$', 'index'),
	(r'^browse', 'browse'),
 )