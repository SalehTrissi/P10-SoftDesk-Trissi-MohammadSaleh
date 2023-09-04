from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(blank=False)
    has_consent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
