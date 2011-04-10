from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from datetime import datetime

urlpatterns = patterns('',
    # Example:
    # (r'^m2m/', include('m2m.foo.urls')),
    
    #(r'^', 'problems.views.sitewide'), # for maintenance, etc
    
    (r'^monkeybutter$', 'search.views.test'),
    
    (r'^$', 'search.views.index'),
    #(r'^?q=([a-zA-Z0-9]*)$','search.views.results' ),
    (r'^results/', include('search.urls')),
    
    #(r'^requests', 'problems.views.requests'), # for maintenance, etc
    (r'^requests/', include('requests.urls')),
    
    (r'^polls', 'problems.views.polls'), # for maintenance, etc
    (r'^polls/', include('polls.urls')),
    
    #(r'^servers', 'problems.views.browseNet'), # for maintenance, etc
    (r'^servers/', include('browseNet.urls')),
    
    #(r'^(news|comments)/', 'problems.views.news'), # for maintenance, etc
    (r'^news/', include('basic.blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (r'^stats', 'problems.views.stats'), # for maintenance, etc
    (r'^stats/', include('stats.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
)
