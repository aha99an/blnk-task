from django.db import models
from users.models.user_model import User


class Fund(models.Model):
    max_amount = models.IntegerField()
    min_amount = models.IntegerField()
    rate = models.FloatField()
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class ProviderFund(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.provider
