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


class IssueSerializer(serializers.ModelSerializer):
    issue_id = serializers.ReadOnlyField(source='id')
    author = serializers.ReadOnlyField(source='author.username')
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'desc', 'tag', 'priority',
                  'status', 'author', 'assignee', 'created_time']

    def validate_assignee(self, assignee):
        user_id = User.objects.get(username=assignee).id
        if not Contributor.objects.filter(
                       user=user_id, project=self.context['project']).exists():
            error_message = 'The assignee '\
                            + str(assignee)\
                            + ' is not registered for the project.'
            raise serializers.ValidationError(error_message)
        return assignee