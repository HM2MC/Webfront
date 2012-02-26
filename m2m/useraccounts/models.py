from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from m2m.stats.models import Log
from m2m.browseNet.models import Host
from m2m.courses.models import Course, Major
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    # security stuff
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)
    
    # ---------------------
    # who is this person?
    #
    studentid = models.IntegerField(unique=True)
    
    nname = models.CharField(max_length=10, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
        
    major = models.ForeignKey(Major, null=True, blank=True)
    taken_courses = models.ManyToManyField(Course, null=True, blank=True)
    
    friends = models.ManyToManyField(User, related_name='friend_to', null=True)
    description = models.TextField(null=True, blank=True)
    
    #
    # ----------------------
    
    # ----------------------
    # where is this person?
    #
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
    dorm = models.IntegerField(choices=DORMS, default=5, null=True, blank=True)
    room = models.CharField(max_length=4,null=True, blank=True)
    #
    # ----------------------
    
    # ----------------------
    # Does M2M care about them?
    hosts = models.ManyToManyField(Host,null=True, blank=True)
    
    #
    # ---------------------
    @models.permalink
    def get_absolute_url(self):
        return ('view_user', None, {'username': self.user.username})

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
post_save.connect(create_user_profile, sender=User)