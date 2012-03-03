from django.db import models
from django.contrib.auth.models import User

from m2m.browseNet.models import Host
# Create your models here.

class CompletedRequestManager(models.Manager):
    def get_query_set(self):
        return super(CompletedRequestManager, self).get_query_set().filter(completed=True)

class OpenRequestManager(models.Manager):
    def get_query_set(self):
        return super(OpenRequestManager, self).get_query_set().filter(completed=False)


# a cleaned up version of the old comments model, django-ready.
class Comment(models.Model):
    CID = models.IntegerField(primary_key=True,unique=True,editable=False,)
    requestTime = models.DateTimeField()
    name = models.CharField(max_length=120,null=True,blank=True,default='Anonymous')
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(max_length=180,null=True,blank=True) 
    completed = models.BooleanField()
    completedTime = models.DateTimeField(null=True,blank=True)
    completerComment = models.TextField(null=True,blank=True)
    completingName = models.CharField(max_length=120,null=True,blank=True) 
    completingServer = models.CharField(max_length=120,null=True,blank=True) 
    isDeleted = models.BooleanField()
    deleterIP = models.IPAddressField(null=True,blank=True)
    deletedTime = models.DateTimeField(null=True,blank=True)
    request = models.TextField()
    server = models.CharField(max_length=60, null=True,blank=True)
    requestIP = models.IPAddressField(max_length=64,null=True,blank=True)
    # ala facebook
    Likes = models.IntegerField(default=0)

    target_host = models.ForeignKey(Host, null=True, blank=True)

    objects = models.Manager()
    completed_objects = CompletedRequestManager()
    open_objects = OpenRequestManager()

    
        
    def __unicode__(self):
        return self.request
    
    class Meta:
        db_table = 'requests_comment' # this is necessary due to a namespace conflict from a recently installed library
    
    def save(self,*args,**kwargs):
        if not self.CID:
            i = Comment.objects.raw('SELECT * FROM requests_comment ORDER BY CID DESC LIMIT 1')[0]
            self.CID = i.CID+1
        super(Comment,self).save(*args,**kwargs)