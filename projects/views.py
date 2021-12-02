from rest_framework import permissions, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer
from .permissions import IsProjectOverseer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOverseer]

    def create(self, request):
        serializer = ProjectSerializer(
            context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            contributor = Contributor(
                user=self.request.user,
                project=Project.objects.last(),
                permission='overseer',
                role='Overseer',
            )
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)