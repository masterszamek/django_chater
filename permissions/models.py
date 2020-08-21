from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.


class ScopePermission(models.Model):
    label = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$', message="Invalid label")],
    )

class Permission(models.Model):
    
    label = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$', message="Invalid label")],
    )
    scope_permission = models.ForeignKey(ScopePermission, on_delete=models.CASCADE)
    description = models.TextField()

class PermissionUserInstance(models.Model):
    

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.BooleanField(default=False)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    # foreignKey to related model
    class Meta:
        abstract = True


class LevelPermissionUserInstance(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level_permission = models.PositiveSmallIntegerField()
    # foreignKey to related model
    class Meta:
        abstract = True

