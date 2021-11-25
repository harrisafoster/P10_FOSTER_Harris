from django.db import models
from django import forms
from django.conf import settings


type_options = (
    ('back-end', 'Back-end'),
    ('front-end', 'Front-end'),
    ('android', 'Android'),
    ('iOS', 'iOS'),
)

permission_options = (
    ('author', 'Author'),
    ('contributor', 'Contributor'),
)

priority_options = (
    ('high', 'High'),
    ('mid', 'Mid'),
    ('low', 'Low'),
)

status_options = (
    ('to do', 'To do'),
    ('doing', 'Doing'),
    ('done', 'Done')
)

tag_options = (
    ('bug', 'Bug'),
    ('task', 'Task'),
    ('improvement', 'Improvement'),
)


class Project(models.Model):
    # links to contributors, issues, users (optional)
    # project_id = ?
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(choices=type_options, max_length=128)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Contributor(models.Model):
    # linked to projects, users
    user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(
        to=Project,
        related_name='contributors',
        on_delete=models.CASCADE)
    permission = forms.ChoiceField(choices=permission_options)
    role = models.CharField(max_length=128)


class Issue(models.Model):
    # linked to users, projects, comments
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(choices=tag_options, max_length=128)
    priority = models.CharField(choices=priority_options, max_length=128)
    project_id = models.ForeignKey(
        to=Project,
        related_name='issues',
        on_delete=models.CASCADE)
    status = models.CharField(choices=status_options, max_length=128)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='issue_author')
    assignee_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        related_name='assignee', null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']


class Comment(models.Model):
    # linked to issues, users
    # comment_id = ?
    description = models.TextField(max_length=2048)
    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(
        to=Issue,
        related_name='comments',
        on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_time']
