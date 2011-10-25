from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from m2m.browseNet.models import Host

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    
    studentid = models.IntegerField(unique=True)
    
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    nname = models.CharField(max_length=10)
    
    hosts = models.ManyToManyField(Host)
    
    
    description = models.TextField(blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('view_user', None, {'username': self.user.username})

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
post_save.connect(create_user_profile, sender=User)