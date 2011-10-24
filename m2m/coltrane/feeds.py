from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.exceptions import ObjectDoesNotExist

from m2m.coltrane.models import Entry, Category

current_site = Site.objects.get_current()

class LatestEntriesFeed(Feed):
    author_name = "Haak Saxberg"
    copyright = "http://{}/flat/copyright/".format(current_site.domain)
    description = "Latest entries posted to {}".format(current_site.name)
    feed_type = Atom1Feed
    item_copyright = copyright
    item_author_name = author_name
    item_author_link = "http://{}/".format(current_site.domain)
    link = "/feeds/entries"
    title = "{}: Latest Entries".format(current_site.name)
    
    def items(self):
        return Entry.live.all()[:15]
    
    def item_pubdate(self, item):
        return item.pub_date
    
    def item_guid(self, item):
        return "tag:{},{}:{}".format(current_site.domain,
                                     item.pub_date.strftime("%Y-%m-%d"),
                                     item.get_absolute_url())
        
    def item_categories(self, item):
        return [c.title for c in item.categories.all()]
    
class CategoryFeed(LatestEntriesFeed):
    
    def get_object(self, request, bits):
        if len(bits) < 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits)
    
    def title(self, obj):
        return "{}: Latest entries in category '{}'".format(current_site.name,
                                                            obj.title)
    def description(self, obj):
        return "{}: Latest entries in category '{}'".format(current_site.name,
                                                            obj.title)
    def link(self, obj):
        return obj.get_absolute_url()
    
    def items(self, obj):
        return obj.live_entry_set()[:15]