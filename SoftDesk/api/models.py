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

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """
    Represents the relationship between users and projects
    """

    # User who is a contributor (foreign key to User model)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Project to which the user is a contributor (foreign key to Project model)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
