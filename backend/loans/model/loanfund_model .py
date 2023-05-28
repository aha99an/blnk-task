from django.db import models

# Create your models here.
class LoanFund(models.Model):
    max_amount = models.IntegerField()
    min_amount = models.IntegerField()
    rate = models.FloatField()
    duration = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
