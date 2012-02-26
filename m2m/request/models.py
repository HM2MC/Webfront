from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# a cleaned up version of the old comments model, django-ready.
class Comment(models.Model):
    CID = models.IntegerField(primary_key=True,unique=True,editable=False,)
    requestTime = models.DateTimeField()
    name = models.CharField(max_length=120,null=True,blank=True,default='Anonymous')
    user = models.ForeignKey(User, null=True)
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
    
    def __unicode__(self):
        return self.request
    
    class Meta:
        db_table = 'requests_comment' # this is necessary due to a namespace conflict from a recently installed library
    
    def save(self,*args,**kwargs):
        if not self.CID:
            i = Comment.objects.raw('SELECT * FROM requests_comment ORDER BY CID DESC LIMIT 1')[0]
            self.CID = i.CID+1
        super(Comment,self).save(*args,**kwargs)