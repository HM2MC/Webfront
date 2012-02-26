from django.db import models
from django.contrib.auth.models import User

import datetime


# Create your models here.

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User)
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    users = models.ManyToManyField(User)
    
    @property
    def votes(self):
        return self.users.count()
    
    def __unicode__(self):
        return self.choice