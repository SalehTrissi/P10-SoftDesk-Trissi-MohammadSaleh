from django.db.models import Q
from rest_framework import generics, status
from .models import Project, Issue, Comment
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from .permissions import IsContributorToProject, CanUpdateOrDeleteComment, CanUpdateOrDeleteIssue


# Create your views here.


class ProjectListCreateView(generics.ListCreateAPIView):

    # Use the ProjectSerializer for serialization
    serializer_class = ProjectSerializer
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]

    # Get projects where the authenticated user is the author
    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        # Set the author to the authenticated user
        serializer.save(author=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Get all Project objects from the database
    queryset = Project.objects.all()
    # Use the ProjectSerializer for serialization
    serializer_class = ProjectSerializer
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated, IsContributorToProject]

    def get_object(self):
        # Retrieve the project instance
        obj = super().get_object()
        # Check if the user is the author or a contributor
        if not (obj.author == self.request.user or IsContributorToProject().has_object_permission(self.request, self, obj)):
            # If not, raise a PermissionDenied exception with a friendly message
            raise PermissionDenied(
                detail="You do not have permission to access this project.")
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is the author or has permission to delete
        if instance.author == request.user or IsContributorToProject().has_object_permission(request, self, instance):
            instance.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You do not have permission to delete this project"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Check if the user is the author or has permission to update
        if instance.author == request.user or IsContributorToProject().has_object_permission(request, self, instance):
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"message": "Project updated successfully"})
        else:
            return Response({"message": "You do not have permission to update this project"}, status=status.HTTP_403_FORBIDDEN)


class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    # Define the behavior when creating a new issue
    def perform_create(self, serializer):
        # Assign the currently logged-in user as the creator of the issue
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        # Add the created_by field to the request data before creating the issue
        request.data["created_by"] = self.request.user.id
        return super().create(request, *args, **kwargs)

    # Filter the queryset to show only issues related to projects where the user is a contributor
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Issue.objects.filter(Q(created_by=user) | Q(project_id__contributors=user))
        return Issue.objects.none()


class IssueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, CanUpdateOrDeleteIssue]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is allowed to delete the issue
        if self.check_permission(instance):
            instance.delete()
            return Response({"message": "Issue deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You do not have permission to delete this issue"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Check if the user is allowed to update the issue
        if self.check_permission(instance):
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"message": "Issue updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You do not have permission to update this issue"}, status=status.HTTP_403_FORBIDDEN)

    def check_permission(self, issue):
        # Check if the user is the author of the issue or has permission to update/delete
        return issue.created_by == self.request.user or CanUpdateOrDeleteIssue().has_object_permission(self.request, self, issue)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    # Define the behavior when creating a new comment
    def perform_create(self, serializer):
        # Assign the currently logged-in user as the creator of the comment
        serializer.save(created_by=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanUpdateOrDeleteComment]
