from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Permission(models.Model):
    name = models.CharField(max_length=30)



class PermissionPerInstance(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.BooleanField(default=False)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    #instance object
    class Meta:
        abstract = True

class LevelPermissionPerInstance(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level_permission = models.PositiveSmallIntegerField()
    #instance obJect
    class Meta:
        abstract = True