from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from users.custom_permissions import IsBanker, IsProvider

from balance.models import Balance
from funds.models import Fund, ProviderFund
from funds.serializers import FundSerializer, ProviderFundSerializer


class FundViewSet(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated, IsBanker]

    def create(self, request, *args, **kwargs):
        data = request.data

        if int(data["min_amount"]) >= data["max_amount"]:
            return JsonResponse(
                data={"message": "Sorry the minimum amount must be less than maximum amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


class ProviderFundViewSet(viewsets.ModelViewSet):
    queryset = ProviderFund.objects.all()
    serializer_class = ProviderFundSerializer
    permission_classes = [IsAuthenticated, IsProvider]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["provider"] = request.user.pk
        fund_amount = int(data["amount"])
        fund = Fund.objects.get(id=data["fund"])

        if fund.min_amount <= fund_amount and fund.max_amount >= fund_amount:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            total_rate = fund.rate * fund.duration
            returns = (fund_amount * total_rate) / 100
            total_money = fund_amount + returns
            balance = Balance.get_solo()
            balance.balance = balance.balance + fund_amount
            balance.save()
            return JsonResponse(
                data={
                    "message": "Fund created successfully."
                    + "Your fund with amount= "
                    + str(fund_amount)
                    + ", your returns= "
                    + str(returns)
                    + ", you will get "
                    + str(total_money)
                    + ", after "
                    + str(fund.duration)
                    + " years."
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            return JsonResponse(
                data={"message": "Error: please enter correct amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request):
        # get
        self.queryset = Fund.objects.all()
        self.serializer_class = FundSerializer
        amount = request.GET.get("amount")
        if amount:
            self.queryset = Fund.objects.filter(
                min_amount__lte=int(amount), max_amount__gte=int(amount)
            )

        return super().list(self, request)
