from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(blank=False)
    consent = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Make a new member active & staff by default, so it can do CRUD operations
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)