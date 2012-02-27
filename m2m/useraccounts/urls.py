from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('useraccounts.views',
                       (r'^$', 'view_home'),
                       (r'^profile/$', 'view_home'),
                       url(r'^login/$', login, name="login"),
                       url(r'^logout/$', logout, name="logout"),
                       )