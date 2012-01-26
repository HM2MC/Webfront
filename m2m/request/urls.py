from django.conf.urls.defaults import *

# Urls go here!

urlpatterns = patterns('request.views',
        
        (r'^$','open'),
        (r'^(?P<page>\d*)$','open'),
        (r'^completed(/(?P<page>\d*))?$','completed'),
        (r'^deleted(/(?P<page>\d*))?$','deleted'),
        (r'^edit/(\d+)$','edit'),
        (r'^complete/(\d+)$','complete'),
        (r'^delete/(\d+)$','delete'),
		(r'^like/(?P<id>\d+)/(?P<page>\d+)$','like'),
    )