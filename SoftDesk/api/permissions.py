from rest_framework import permissions


class IsContributorToProject(permissions.BasePermission):
    """
    Custom permission to check if the user is a contributor to a project.
    """

    def has_object_permission(self, request, view, obj):
        # Allow access if the request user is the author of the project
        return obj.author == request.user or obj.contributors.filter(user=request.user).exists()


class CanUpdateOrDeleteRequest(permissions.BasePermission):
    """
    Custom permission to check if the user can update or delete a request.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the request
        return obj.created_by == request.user


class CanUpdateOrDeleteIssue(permissions.BasePermission):
    """
    Custom permission to check if the user can update or delete an issue.
    """

    def has_object_permission(self, request, view, obj):
        # Debug messages to check values
        print(f"request.user: {request.user}")
        print(f"obj.created_by: {obj.created_by}")

        # Check if the user is the author of the issue
        has_permission = obj.created_by == request.user

        # Debug message for permission result
        print(f"Permission result: {has_permission}")

        return has_permission


class CanUpdateOrDeleteComment(permissions.BasePermission):
    """
    Custom permission to check if the user can update or delete a comment.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the comment
        if obj.created_by == request.user:
            return True

        # Check if the user is a contributor to the project or the project's author
        project = obj.issue.project
        return project.contributors.filter(pk=request.user.pk).exists() or project.author == request.user
