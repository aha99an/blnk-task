from funds.models import Fund, ProviderFund
from rest_framework import serializers


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ["id", "max_amount", "min_amount", "rate", "duration"]


class ProviderFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderFund
        fields = "__all__"
