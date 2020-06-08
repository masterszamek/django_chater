from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions  as rest_permissions

from rest_framework import viewsets, mixins, views
from rest_framework import decorators

from . import models
from . import serializers
from . import permissions



class IdeaViewSet(viewsets.ModelViewSet):

    queryset = models.Idea.objects.all()
    permission_classes = [rest_permissions.IsAuthenticated, permissions.IsOwnerOrStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return serializers.ReadOnlyIdeaSerializer
        else:
            return serializers.CreateIdeaSerializer


class WhatsNewViewSet(viewsets.ModelViewSet):
    queryset = models.WhatsNew.objects.all()
    serializer_class = serializers.WhatsNewSerializer
    permission_classes = [rest_permissions.IsAuthenticated, rest_permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [rest_permissions.IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]



#list  create retrieve update partial_update destroy