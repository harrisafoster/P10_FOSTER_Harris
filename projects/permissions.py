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