from django.contrib import admin
from . import models

admin.site.register(models.IdeaCategory)
admin.site.register(models.IdeaTag)
admin.site.register(models.IdeaComment)
admin.site.register(models.Idea)
