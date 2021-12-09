from rest_framework import permissions, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsProjectOverseer, IsProjectOverseerUser, IsProjectContributor


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

    def destroy(self, request, pk=None):
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


class IssueViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]
    model = Issue

    def create(self, request, parent_lookup_project):
        project = get_object_or_404(Project, pk=parent_lookup_project)
        self.check_object_permissions(request, project)
        serializer = IssueSerializer(
            data=request.data, context={'request': request, 'project': parent_lookup_project})
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                project=Project.objects.get(pk=parent_lookup_project)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, parent_lookup_project):
        #TODO have to enter all fields again, maybe we can keep unchanged values ?
        queryset = Issue.objects.filter(pk=pk, project=parent_lookup_project)
        issue = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue,
                                     data=request.data,
                                     context={'request': request,
                                              'project': parent_lookup_project})
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                project=Project.objects.get(pk=parent_lookup_project)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, parent_lookup_project):
        queryset = Issue.objects.filter(pk=pk, project=parent_lookup_project)
        issue = get_object_or_404(queryset, pk=pk)
        comments = Comment.objects.filter(issue=pk)
        self.check_object_permissions(request, issue)
        issue.delete()
        for comment in comments:
            comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectContributor]

    def list(self, request, parent_lookup_project, parent_lookup_issue):
        if not Issue.objects.filter(pk=parent_lookup_issue).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        project = get_object_or_404(Project, pk=parent_lookup_project)
        self.check_object_permissions(request, project)
        queryset = Comment.objects.filter(
            issue__project=parent_lookup_project,
            issue=parent_lookup_issue
        )
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk, parent_lookup_project, parent_lookup_issue):
        queryset = Comment.objects.filter(
            pk=pk,
            issue__project=parent_lookup_project,
            issue=parent_lookup_issue
        )
        comment = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request, parent_lookup_project, parent_lookup_issue):
        if not Issue.objects.filter(pk=parent_lookup_issue, project=parent_lookup_project).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        issue = Issue.objects.get(pk=parent_lookup_issue)
        self.check_object_permissions(request, issue)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                issue=Issue.objects.get(pk=parent_lookup_issue)
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, parent_lookup_project, parent_lookup_issue):
        if not Issue.objects.filter(pk=parent_lookup_issue, project=parent_lookup_project).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment = get_object_or_404(Comment, pk=pk, issue=parent_lookup_issue)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=self.request.user,
                issue=Issue.objects.get(pk=parent_lookup_issue)
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, parent_lookup_project, parent_lookup_issue):
        if not Issue.objects.filter(pk=parent_lookup_issue).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment = get_object_or_404(Comment, pk=pk, issue=parent_lookup_issue)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)