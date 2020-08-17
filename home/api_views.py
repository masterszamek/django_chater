from django.contrib.auth.models import User


from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions as rest_permissions

from rest_framework import viewsets, mixins, generics, views
from rest_framework import decorators

from . import models
from . import serializers
from . import permissions




class IdeaCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.IdeaCategory.objects.all()
    serializer_class = serializers.IdeaCategorySerializer

class IdeaTagViewSet(viewsets.ModelViewSet):
    queryset = models.IdeaTag.objects.all()
    serializer_class = serializers.IdeaCategorySerializer

class IdeaViewSet(viewsets.ModelViewSet):
    queryset = models.Idea.objects.all()
    serializer_class = serializers.IdeaSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update" or self.action == "update":
            return serializers.CreateIdeaSerializer
        return serializers.IdeaSerializer


    def get_queryset(self):
        print(self.kwargs)
        return models.IdeaCategory.objects.filter(id=self.kwargs['idea_category_pk'])[0].ideas
    

class IdeaCommentViewSet(viewsets.ModelViewSet):
    queryset = models.IdeaComment.objects.all()
    serializer_class = serializers.IdeaCommentSerializer


    def get_queryset(self):
        print(self.kwargs)
        return models.Idea.objects.filter(id=self.kwargs['idea_pk'])[0].comments



class CreateUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer


class CreateQuestionToAuthor(mixins.CreateModelMixin, viewsets.GenericViewSet):
    

#list  create retrieve update partial_update destroy