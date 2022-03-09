from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    follow = models.ManyToManyField(
        "self", blank=True, related_name="followers", symmetrical=False
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' or 'username'
    REQUIRED_FIELDS = []