from loans.models import Loan, CustomerLoan
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ("id", "max_amount", "min_amount", "rate", "duration")


class CustomerLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoan
        fields = "__all__"


class AmortizationLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoan
        fields = ["id", "amount"]
