from rest_framework import serializers
from . import models

from django.contrib.auth.models import User


class PrioritySerializer(serializers.ModelSerializer):
    color = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()


    def get_priority(self, obj):
        return obj.priority.value  

    def get_color(self, obj):
        return obj.color

    def get_title(self, obj):
        return obj.title


    class Meta:
        model = models.Priority
        fields = "__all__"
        read_only = "__all__"



    
class ReadOnlyIdeaSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    priority = PrioritySerializer()
    can_change = serializers.SerializerMethodField()

    def get_can_change(self, obj):
        user = self.context.get("request").user      

        if user.is_staff or user == obj.author:
            return True
        
        return False

    class Meta:
        model = models.Idea
        fields = '__all__'
        read_only = '__all__'


class CreateIdeaSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()


    def create(self, data):
        user = self.context['request'].user

        return models.Idea(
            title = data['title'],
            text = data['text'],
            author = user,
            priority = data['priority']
        )

    def update(self, instance, data):

        instance.priority = data['priority']
        instance.text = data.get("text", instance.text)
        instance.title = data.get("title", instance.title)
        instance.save()
        return instance

    def save(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).save(*args, **kwargs) #parent method invoke only create 
        self.instance.save()


    class Meta:
        model = models.Idea
        fields = ['title', 'text', 'priority', 'author']
        read_only = ["author"]


class WhatsNewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    def create(self, data):
        user = self.context['request'].user        
        return models.WhatsNew(
            author=user,
            title=data['title'],
            text=data['text'],
        )

    def update(self, instance, data):
        instance.text = data.get('text', instance.text)
        instance.title = data.get('title', instance.title)
        instance.save()
        return instance

    def save(self, *args, **kwargs):
        super(serializers.ModelSerializer, self).save(*args, **kwargs) #parent method invoke only create 
        self.instance.save()

        
    class Meta:
        model = models.WhatsNew
        fields = "__all__"
