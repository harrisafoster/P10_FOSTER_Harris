from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator

from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']


class ContributorSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'permission', 'role']
        validators = [
            UniqueTogetherValidator(
                queryset=Contributor.objects.all(),
                fields=['user', 'project'],
            ),
        ]