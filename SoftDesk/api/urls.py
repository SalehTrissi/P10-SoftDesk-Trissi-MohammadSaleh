from django.urls import path
from .views import CommentListCreateView, CommentRetrieveUpdateDestroyView
from .views import ProjectListCreateView, ProjectDetailView, IssueListCreateView, IssueRetrieveUpdateDestroyView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(),
         name='project-list'),  # List and create projects
    path('projects/<int:pk>/', ProjectDetailView.as_view(),
         name='project-detail'),  # Retrieve, update, delete projects
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('issues/<int:pk>/', IssueRetrieveUpdateDestroyView.as_view(),
         name='issue-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<uuid:pk>/',
         CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
]
