from rest_framework import permissions

from .models import Project, Contributor, Issue, Comment


class IsProjectOverseer(permissions.BasePermission):
    """
    Verification: user is authenticated => Permissions allowed to create projects.
    Verification: user is project overseer => Permissions allowed to edit/delete own project(s)
    """
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True

        elif Contributor.objects.filter(
                user=request.user, project=obj).exists():
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return Contributor.objects.get(
                        user=request.user, project=obj).permission == 'overseer'

        else:
            return False


class IsProjectContributor(permissions.BasePermission):
    """
    Verification: User is contributor => contributor permissions accorded
    """
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            if isinstance(obj, Project):
                return Contributor.objects.filter(
                    user=request.user, project=obj).exists()
            elif isinstance(obj, Issue):
                return Contributor.objects.filter(
                    user=request.user, project=obj.project).exists()
            elif isinstance(obj, Comment):
                return Contributor.objects.filter(
                    user=request.user, project=obj.issue.project).exists()
        else:
            return obj.author == request.user


class IsCommentAuthor(permissions.BasePermission):
    """
    Verification: user is contributor => permission accorded to view/create comments
    Verification: user is author of comment => permission accorded to edit/delete own comments
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(
                    user=request.user, project=obj).exists()

        elif request.method == 'POST':
            return Contributor.objects.filter(
                    user=request.user, project=obj.project).exists()

        elif request.method == 'DELETE':
            return Comment.objects.filter(
                author=request.user, issue=obj.issue).exists()

        elif request.method == 'PUT':
            return Comment.objects.filter(
                author=request.user, issue=obj.issue).exists()

        else:
            return False


class IsIssueAuthor(permissions.BasePermission):
    """
    Verification: user is contributor => permission accorded to create/view issues
    Verification: user is issue author => permission accorded to edit/delete own issues
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(
                    user=request.user, project=obj.project).exists()

        elif request.method == 'POST':
            return Contributor.objects.filter(
                    user=request.user, project=obj).exists()

        elif request.method == 'DELETE':
            return Issue.objects.filter(
                author=request.user, project=obj.project).exists()

        elif request.method == 'PUT':
            return Issue.objects.filter(
                author=request.user, project=obj.project).exists()

        else:
            return False


class IsProjectOverseerUser(permissions.BasePermission):
    """
    Verification: user is project contributor => permissions accorded to view contributors
    Verification: user is project author => permissions accorded to create/edit/delete contributors
    Verification: there is more than one project overseer => permission accorded to delete one of the overseers
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(
                    user=request.user, project=obj.project).exists()

        elif request.method == 'DELETE':
            return Contributor.objects.filter(
                    user=request.user, project=obj.project,
                    permission='overseer').exists() \
                    and (Contributor.objects.filter(
                        permission='overseer', project=obj.project).count() > 1
                        or obj.permission == 'contributor')

        elif request.method == 'POST':
            return Contributor.objects.filter(
                    user=request.user, project=obj, permission='overseer').exists()

        elif request.method == 'PUT':
            return Contributor.objects.filter(
                user=request.user, project=obj.project, permission='overseer').exists()

        else:
            return False
