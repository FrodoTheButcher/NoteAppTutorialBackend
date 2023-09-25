from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False)
    description = models.TextField(blank=False,null=False)
    user = models.ForeignKey(User,blank=False,null=False,on_delete=models.CASCADE)
    updateDate = models.DateTimeField(auto_now=True)
    createDate = models.DateTimeField(auto_now_add=True)
    expireDate = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.name