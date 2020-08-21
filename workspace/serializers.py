from . import models
from rest_framework import serializers
from rest_framework.serializers import ValidationError as drf_ValidationError



class IsPasswordAbstract():
    """Prevent from copy-paste, just inheritance"""

    is_password = serializers.SerializerMethodField()
    def get_is_password(self, obj):
        if obj.password:
            return True
        return False

class WorkspaceSerializer(IsPasswordAbstract, serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Workspace
        exclude = ["password"]

    
    
    
class ListWorkspaceSerializer(IsPasswordAbstract, serializers.ModelSerializer):

    class Meta:
        model = models.Workspace
        fields = ["name", "is_password"]



class RoomSerializer(IsPasswordAbstract, serializers.Room):
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Workspace
        exclude = ["password"]

 

class ListRoomSerializer(IsPasswordAbstract, serializers.Room):


    class Meta:
        model = models.Workspace
        fields = ["name", "is_password"]

