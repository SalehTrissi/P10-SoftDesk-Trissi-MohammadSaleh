from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(default=0)
    has_consent = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Override the save method to set the username based on the email address.
    def save(self, *args, **kwargs):
        if self._state.adding:
            # Generate a username from the email address by taking the part before '@'.
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
