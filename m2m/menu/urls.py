from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

# Urls go here!

urlpatterns = patterns('menu.views',
    (r'^$', 'main'),
    
    
    )