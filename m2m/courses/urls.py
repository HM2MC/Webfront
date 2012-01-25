from django.conf.urls.defaults import *


urlpatterns = patterns('courses.views',
	(r'^$', 'index'),
	(r'^browse', 'browse'),
	(r'^calendar', 'calendar'),
	(r'^query', 'course_match')
 )