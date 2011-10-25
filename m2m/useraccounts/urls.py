from django.conf.urls.defaults import *

urlpatterns = patterns('useraccounts.views',
                       (r'^signup', 'signup'),
                       (r'^home', 'view_home'),
                       (r'^login', 'login'),
                       )