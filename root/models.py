from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Priority(models.Model):
    class PriorityChoice(models.IntegerChoices):
        HIGH = 1, _("High task priority")
        MEDIUM = 2, _("Medium task priority")
        LOW = 3, _("Low task priority")
    
    class Color(models.TextChoices):
        HIGH = "#FFB6C1", _("light pink")
        MEDIUM = "#99EE99", _("light green")
        LOW = "#20B2D0", _("light blue")

    priority = models.IntegerField(choices=PriorityChoice.choices, default=3, unique=True, blank=False)
    
    @property
    def color(self):
        return self.Color[self.PriorityChoice(self.priority).name].value
    
    @property
    def title(self):
        return self.__str__()
        
    def __str__(self):
        return str(self.PriorityChoice(self.priority).label)

class Idea(models.Model):


    author = models.ForeignKey(User, blank=False, on_delete=models.SET(get_sentinel_user))
    title = models.CharField(max_length=50, blank=False)
    text = models.TextField()
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} -> {}".format(self.title, self.text)

    class Meta:
        ordering = ['send_date']


class WhatsNew(models.Model):
    author = models.ForeignKey(User, blank=False, on_delete=models.SET(get_sentinel_user))
    title = models.CharField(max_length=50, blank=False)
    text = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} -> {}".format(self.title, self.text)

    class Meta:
        ordering = ['send_date']