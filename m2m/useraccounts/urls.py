from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout_then_login, password_change, password_change_done

urlpatterns = patterns('useraccounts.views',
                       (r'^$', 'view_home'),
                       (r'^profile/$', 'view_home'),
                       url(r'^reset_password/$', password_change),
                       url(r'^reset_password_done/$', password_change_done),
                       url(r'^login/$', login, name="login"),
                       url(r'^logout/$', logout_then_login, name="logout"),
                       )