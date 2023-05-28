from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
user_type = (
    ("customer", "Customer"),
    ("provider", "Provider"),
    ("banker", "Bank Personnel"),
)


class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=user_type)

    def __str__(self):
        return str(self.id)
