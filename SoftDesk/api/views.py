from rest_framework import generics
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class ProjectListCreateView(generics.ListCreateAPIView):
    # Get all Project objects from the database
    queryset = Project.objects.all()
    # Use the ProjectSerializer for serialization
    serializer_class = ProjectSerializer
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]


# Create a view to retrieve, update, and delete projects
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    # Get all Project objects from the database
    queryset = Project.objects.all()
    # Use the ProjectSerializer for serialization
    serializer_class = ProjectSerializer
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]

# Create a view for listing and creating issues


class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    # Define the behavior when creating a new issue
    def perform_create(self, serializer):
        # Assign the currently logged-in user as the creator of the issue
        serializer.save(created_by=self.request.user)

    # Filter the queryset to show only issues related to projects where the user is a contributor
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Issue.objects.filter(project_id__contributors=user)
        return Issue.objects.none()

# Create a view for retrieving, updating, and deleting individual issues


class IssueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]
