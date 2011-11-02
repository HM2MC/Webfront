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
    
    nname = models.CharField(max_length=10)
    birthday = models.DateField()
    
    DORMS = (
             (1,'East' ),
             (2,'West'),
             (3,'North' ),
             (4,'South'),
             (5,'Atwood'),
             (6,'Case'),
             (7,'Sontag'),
             (8,'Linde'),
             (9,'CGU'),
             (10,'BPA'),
            )
    dorm = models.IntegerField(choices=DORMS, default=5)
    room = models.IntegerField()
    
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