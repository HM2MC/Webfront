from django.conf.urls.defaults import patterns

from django.views.generic import ArchiveIndexView, DetailView

from m2m.coltrane.models import Entry

entry_info_dict = {
                   'queryset': Entry.live.all(),
                   'date_field': 'pub_date',
                   'paginate_by': 5,
                   }

urlpatterns = patterns('',
        (r'^((?P<page>\d+)/)?$', 
        ArchiveIndexView.as_view(**entry_info_dict), entry_info_dict, 'coltrane_entry_archive_index'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DetailView.as_view(model=Entry), {'news':'current'}, 'coltrane_entry_detail'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
        'django.views.generic.date_based.archive_day', entry_info_dict, 'coltrane_entry_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        'django.views.generic.date_based.archive_month', entry_info_dict, 'coltrane_entry_archive_month'),
    (r'^(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year', entry_info_dict, 'coltrane_entry_archive_year'),
       )