from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(default=0)
    has_consent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
