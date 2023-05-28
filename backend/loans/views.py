from rest_framework import viewsets
from loans.models import Loan, CustomerLoan
from loans.serializers import (
    AmortizationLoanSerializer,
    LoanSerializer,
    CustomerLoanSerializer,
)
from rest_framework import status
from django.http import JsonResponse
from loans.utils import get_loan_settlement_amount, get_same_day_from_next_months
from balance.models import Balance
from rest_framework.permissions import IsAuthenticated
from users.custom_permissions import IsBanker, IsCustomer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsBanker]

    def create(self, request, *args, **kwargs):
        data = request.data

        if int(data["min_amount"]) >= data["max_amount"]:
            return JsonResponse(
                data={"message": "Sorry the minimum amount must be less than maximum amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


class CustomerLoanViewSet(viewsets.ModelViewSet):
    queryset = CustomerLoan.objects.filter()
    serializer_class = CustomerLoanSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["customer"] = request.user.pk
        loan_amount = int(data["amount"])
        loan_id = data["loan"]
        loan = Loan.objects.get(id=loan_id)

        if not (loan.min_amount <= loan_amount and loan.max_amount >= loan_amount):
            return JsonResponse(
                data={"message": "Error: please enter correct amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=data)
        total_rate = loan.rate * loan.duration
        interest = (loan_amount * total_rate) / 100
        settlement_amount = loan_amount + interest
        balance = Balance.get_solo()

        if balance.balance < loan_amount:
            return JsonResponse(
                data={"message": "Sorry the balance is less than the loan amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        balance.balance = balance.balance - loan_amount
        balance.save()
        return JsonResponse(
            data={
                "message": "Loan created successfully."
                + " Your loan with amount= "
                + str(loan_amount)
                + ", with interest= "
                + str(interest)
                + ", you have to return "
                + str(settlement_amount)
                + ", after "
                + str(loan.duration)
                + " years."
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        # get
        self.queryset = Loan.objects.all()
        self.serializer_class = LoanSerializer
        amount = request.GET.get("amount")
        if amount:
            self.queryset = Loan.objects.filter(
                min_amount__lte=int(amount), max_amount__gte=int(amount)
            )

        return super().list(self, request)


class AmortizationViewSet(viewsets.ModelViewSet):
    queryset = CustomerLoan.objects.all()
    serializer_class = AmortizationLoanSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def list(self, request):
        self.queryset = CustomerLoan.objects.filter(customer_id=request.user.pk)
        return super().list(self, request)

    def retrieve(self, request, pk=None):
        customer_loan = CustomerLoan.objects.get(id=pk)

        settlement_amount = get_loan_settlement_amount(
            loan_amount=customer_loan.amount,
            loan_duration=customer_loan.loan.duration,
            loan_rate=customer_loan.loan.rate,
        )
        # calculate_due_dates
        months = customer_loan.loan.duration * 12
        monthly_amount = settlement_amount / months

        installments = {}
        list_of_installment_dates = get_same_day_from_next_months(
            months_number=months, start_date=customer_loan.created_at
        )

        for installment_date in list_of_installment_dates:
            installments[installment_date] = monthly_amount

        return JsonResponse(data=installments, status=status.HTTP_200_OK)
