from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError as django_ValidationError

from rest_framework import serializers
from rest_framework.serializers import ValidationError as drf_ValidationError

from . import models


class IdeaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IdeaTag
        fields = ['name']

class IdeaSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Idea
        fields = '__all__'

class CreateIdeaSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.RegexField(regex='^[a-zA-Z0-9_]+$', max_length=20),
    )
    
    def create(self, validated_data):
        tags = [models.IdeaTag.objects.get_or_create(name=tag)[0] for tag in validated_data['tags']]
        author = self.context['request'].user
        idea = models.Idea(
                author=author,
                text=validated_data['text'],
                title=validated_data['title'],
                in_progress=validated_data['in_progress'],
                category=validated_data['category'],
            )
        idea.save()
        idea.tags.add(*tags)
        return idea

    def update(self, instance, validated_data):
 
        instance.text = validated_data.get("text", instance.text)
        instance.title = validated_data.get("title", instance.title)
        instance.in_progress = validated_data.get("in_progress", instance.in_progress)
        instance.category = validated_data.get("category", instance.category)
        instance.save()
        if "tags" in validated_data:
            instance.tags.clear()
            tags = [models.IdeaTag.objects.get_or_create(name=tag)[0] for tag in validated_data['tags']]
            instance.tags.add(*tags)
        
        return instance
    

    def to_representation(self, instance):
        data = IdeaSerializer().to_representation(instance)
        return data


    class Meta:
        model = models.Idea
        exclude = ['author']



class IdeaCategorySerializer(serializers.ModelSerializer):
    ideas = IdeaSerializer(many=True, read_only=True)
    class Meta:
        model = models.IdeaCategory
        fields = '__all__'


class IdeaCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    def create(self, validated_data):
        author = self.context['request'].user
        comment = models.IdeaComment(author=author, **validated_data)
        comment.save()
        return comment

    
    class Meta:
        model = models.IdeaComment
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        exclude = ['answered']


class CreateUserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        super(CreateUserSerializer, self).validate(data)

        user = User(**data)
        try:
            print("oooooo")
            validate_password(data['password'], user)
        except django_ValidationError as error:
            
            raise django_ValidationError({'password':[error]})


    class Meta:
        model = User
        fields = ['username', 'password', 'email']

