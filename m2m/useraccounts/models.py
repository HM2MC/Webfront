from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from m2m.stats.models import Log
from m2m.browseNet.models import Host
from m2m.settings import INSTALLED_APPS
#from m2m.courses.models import Course, Major, Section

from itertools import chain
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    # security stuff
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)
    
    # ---------------------
    # who is this person?
    #
    studentid = models.IntegerField(unique=True, null=True) # won't ever be null actually
    
    nname = models.CharField(max_length=10, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    
    phonenumber = models.CharField(max_length=15, blank=True)
        
    #major = models.ForeignKey(Major, null=True, blank=True)
    #taken_courses = models.ManyToManyField(Section, null=True, blank=True)
    
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
    
    @property
    def requests(self):
        """Fetches all requests associated with a user, as a QuerySet. """
        return self.user.comment_set.all() | self.user.supported_requests.all()
    
    def completed_requests(self):
        """Returns all completed requests associated with a user"""
        return self.requests.filter(completed=True)
    
    def open_requests(self):
        """Returns all non-completed requests associated with a user"""
        return self.requests.filter(completed=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_user', None, {'username': self.user.username})

    def __unicode__(self):
        return self.user.username

class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name='friend_set')
    to_friend = models.ForeignKey(User, related_name='to_friend_set')
    
    def __unicode__(self):
        return u"{} --> {}".format(self.from_friend.username, self.to_friend.username)
    
    class Meta:
        unique_together = (('to_friend', 'from_friend'))

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

# request-specific properties; don't add these if the request app isn't installed yet
if 'request' in INSTALLED_APPS:
    User.completed_requests = property(lambda u: u.comment_set.all().filter(completed=True))
    User.open_requests = property(lambda u: u.comment_set.all().filter(completed=False))

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
 
# this signal isn't needed because of the 'profile' property we set on Users above       
#post_save.connect(create_user_profile, sender=User)