from rest_framework import permissions

from .models import Project, Contributor, Issue, Comment


class IsProjectOverseer(permissions.BasePermission):
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


class IsProjectOverseerUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return Contributor.objects.filter(
                    user=request.user, project=obj).exists()

        elif request.method == 'DELETE':
            return Contributor.objects.filter(
                    user=request.user, project=obj.project,
                    permission='overseer').exists() \
                    and (Contributor.objects.filter(
                        permission='overseer', project=obj.project).count() > 1
                        or obj.permission == 'contributor')

        elif request.method == 'POST':
            return Contributor.objects.filter(
                    user=request.user, project=obj, permission='overseer'
                    ).exists()
        else:
            return False