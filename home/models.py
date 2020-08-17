import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator



def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class IdeaCategory(models.Model):
    title = models.CharField(verbose_name="Category title", max_length=50, unique=True)

    def __str__(self):
        return self.title
    

class IdeaTag(models.Model):
    name = models.CharField(
        max_length=20, 
        unique=True,
        db_index=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$', message="Invalid tag name")],
    )

    def __str__(self):
        return self.name
    

class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, unique=True)
    text = models.TextField(unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    in_progress = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="ideas")
    category = models.ForeignKey(IdeaCategory, related_name="ideas", blank=False, on_delete=models.CASCADE)
    tags = models.ManyToManyField(IdeaTag, related_name="ideas", blank=True)

    def __str__(self):
        return "{}: {}".format(self.author, self.title)
    

    class Meta:
        ordering = ['create_date']



class IdeaComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="+")
    text = models.TextField(unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}: {}".format(self.author, self.text)
    
    class Meta:
        ordering = ['create_date']


class QuestionToCreator(models.Model):
    author = models.CharField(
        max_length=30,
        validators=[RegexValidator(regex='^[a-zA-Z]+$', message="Invalid tag name")],
        )
    text = models.TextField(unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['create_date']