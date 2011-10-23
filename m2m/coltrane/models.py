from django.db import models
from django.contrib.auth.models import User

from tagging.fields import TagField
from markdown import markdown

import datetime
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=250, help_text="Max 250 chars")
    slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField()
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def live_entry_set(self):
        from m2m.coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):    
        return "categories/{}".format(self.slug)

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)
    
class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
                      (LIVE_STATUS, "Live"),
                      (DRAFT_STATUS, "Draft"),
                      (HIDDEN_STATUS, "Hidden")
                      )
    
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date=models.DateTimeField(default=datetime.datetime.now)
    
    slug = models.SlugField(unique_for_date='pub_date')
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    
    categories = models.ManyToManyField(Category)
    tags = TagField()
    
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)
    
    
    live = LiveEntryManager()
    objects = models.Manager()
    
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
    
    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)
   
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (), { 
                                              'year': self.pub_date.strftime("%Y"),
                                              'month': self.pub_date.strftime("%b").lower(),
                                              'day': self.pub_date.strftime("%d"),
                                              'slug': self.slug
                                             })
        
class Link(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    url = models.URLField(unique=True)
    
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    
    tags = TagField()
    
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True)
    
    via_name = models.CharField('Via', max_length=250, blank=True,
                                help_text="The name of the person whose site you spotted the link on. Optional.")
    via_url = models.URLField('Via URL', blank=True,
                              help_text="The URL of the site where you spotted the link. Optional.")
    
    class Meta:
        ordering = ['-pub_date']
        
    def __unicode__(self):
        return self.title
    
    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        super(Link, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_link_detail', (), {
                                             'year': self.pub_date.strftime("%Y"),
                                             'month': self.pub_date.strftime("%b"),
                                             'day': self.pub_date.strftime("%d"),
                                             'slug':self.slug
                                             })
    

#from akismet import Akismet
#from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
#from django.contrib.sites.models import Site
#from django.utils.encoding import smart_str
from django.core.mail import mail_managers

def moderate_comment(sender, comment, request, **kwargs):
    if not comment.id:
        entry = comment.content_object
        delta = datetime.datetime.now() - entry.pub_date
        if delta.days > 30:
            comment.is_public = False
    email_body = "{} posted a new comment on the entry '{}'"
    mail_managers("New comment posted",
                  email_body.format(comment.name,
                                    comment.content_object))
    
comment_will_be_posted.connect(moderate_comment, Comment)
            