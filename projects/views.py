from rest_framework import permissions, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import IsProjectOverseer, IsProjectOverseerUser


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


class ContributorViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsProjectOverseerUser]
    model = Contributor
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def create(self, request, parent_lookup_project):
        project = get_object_or_404(Project, pk=parent_lookup_project)
        self.check_object_permissions(request, project)
        data = request.data.copy()
        if 'project' not in data:
            data.update({'project': str(parent_lookup_project)})
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, parent_lookup_project):
        queryset = Contributor.objects.filter(pk=pk, project=parent_lookup_project)
        contributor = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, contributor)
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)