from django.db import models
from django.contrib.auth.models import User

import datetime


# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    
    pub_date = models.DateTimeField('date published')
    expiry_date = models.DateField('date expires', blank=True, null=True)
    
    user = models.ForeignKey(User)
    
    has_voted = models.ManyToManyField(User, related_name='polls_voted_set', null=True, blank=True)
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    users = models.ManyToManyField(User, null=True, blank=True)
    
    @property
    def votes(self):
        return self.users.count()
    
    def __unicode__(self):
        return self.choice