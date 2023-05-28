from django.db import models
from users.models.user_model import User
from solo.models import SingletonModel


class Balance(SingletonModel):
    balance = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.balance)
