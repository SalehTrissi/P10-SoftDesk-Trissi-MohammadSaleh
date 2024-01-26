import uuid
from django.db import models
from users.models import User


class Project(models.Model):
    # Fields for the Project model
    name = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.CharField(
        max_length=20,
        choices=[
            ('back-end', 'Back-End'),
            ('front-end', 'Front-End'),
            ('iOS', 'iOS'),
            ('Android', 'Android'),
        ]
    )

    # Author of the project (a user who created the project)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='projects'
    )

    # Contributors to the project (many-to-many relationship with User through Contributor)
    contributors = models.ManyToManyField(User, through='Contributor')


class Contributor(models.Model):
    """
    Represents the relationship between users and projects
    """

    # User who is a contributor (foreign key to User model)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Project to which the user is a contributor (foreign key to Project model)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    # Define choices for priority and tags
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]

    # Define choices for status
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_issues'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_issues',
        null=True,
        blank=True
    )

    project_id = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default='TASK'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='To Do'
    )


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(
        'Issue', on_delete=models.CASCADE, related_name='comments'
    )
