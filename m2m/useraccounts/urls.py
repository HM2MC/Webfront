from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('useraccounts.views',
                       (r'^profile/$', 'view_home'),
                       (r'^login/$', login),
                       (r'^logout/$', logout),
                       )