from django.db import models
from users.models.user_model import User


class Loan(models.Model):
    max_amount = models.IntegerField()
    min_amount = models.IntegerField()
    rate = models.FloatField()
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class CustomerLoan(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)
