from rest_framework import status
from rest_framework.test import APITestCase
from loans.models import CustomerLoan, Loan
from collections import OrderedDict
from loans.utils import get_same_day_from_next_months
from users.models.user_model import User
from balance.models import Balance
from rest_framework.reverse import reverse


class LoansTests(APITestCase):
    def setUp(self):
        user = User.objects.create(username="ahmed", user_type="banker")
        user.set_password("123456")
        user.save()

        data = {"username": "ahmed", "password": "123456"}
        response = self.client.post("/api/token/", data, format="json")
        self.token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.loans_url = reverse("loans:loan-list")

    def test_create_loan(self):
        data = {"max_amount": 2000, "min_amount": 1000, "rate": 10, "duration": 10}

        response = self.client.post(self.loans_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.last().max_amount, 2000)
        self.assertEqual(Loan.objects.last().min_amount, 1000)
        self.assertEqual(Loan.objects.last().rate, 10)
        self.assertEqual(Loan.objects.last().duration, 10)
    
    def test_create_loan_min_amount_bigger_than_max_amount(self):
        data = {"max_amount": 1000, "min_amount": 2000, "rate": 10, "duration": 10}

        response = self.client.post(self.loans_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        
        self.assertEqual(response.json()["message"], "Sorry the minimum amount must be less than maximum amount")


    def test_get_loan(self):
        loan = Loan.objects.create(
            max_amount=2000, min_amount=1000, rate=10, duration=10
        )
        response = self.client.get(self.loans_url, format="json")

        loan.refresh_from_db()
        self.assertEqual(
            response.data["results"][0],
            OrderedDict(
                {
                    "id": 1,
                    "max_amount": loan.max_amount,
                    "min_amount": loan.min_amount,
                    "rate": loan.rate,
                    "duration": loan.duration,
                }
            ),
        )


class CustomerLoanTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="ahmed", user_type="customer")
        user.set_password("123456")
        user.save()

        data = {"username": "ahmed", "password": "123456"}
        self.loan1 = Loan.objects.create(
            max_amount=2000, min_amount=1000, rate=20, duration=1
        )
        self.loan2 = Loan.objects.create(
            max_amount=10000, min_amount=5000, rate=20, duration=2
        )

        response = self.client.post("/api/token/", data, format="json")
        self.token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.customer_loan_url = reverse("loans:custmer-loan-list")

    def test_create_customerLoan(self):
        data = {"loan": self.loan1.pk, "amount": 1500}
        response = self.client.post(self.customer_loan_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["message"], "Sorry the balance is less than the loan amount"
        )

    def test_create_customerLoan_balance_bigger_than_loan(self):
        Balance.objects.create(balance=1500)

        data = {"loan": self.loan1.pk, "amount": 1500}
        response = self.client.post(self.customer_loan_url, data, format="json")

        self.assertEqual(
            response.json()["message"],
            "Loan created successfully. "
            + "Your loan with amount= "
            + "1500"
            + ", with interest= "
            + "300.0"
            + ", you have to return "
            + "1800.0"
            + ", after "
            + "1"
            + " years.",
        )

    def test_create_customerLoan_with_wrong_amount(self):
        data = {"loan": 1, "amount": 500}
        response = self.client.post(self.customer_loan_url, data, format="json")
        self.assertEqual(
            response.json()["message"], "Error: please enter correct amount"
        )

    def test_get_customerLoan(self):
        response = self.client.get(self.customer_loan_url, format="json")

        self.assertEqual(
            response.data["results"],
            [
                OrderedDict(
                    {
                        "id": self.loan1.id,
                        "max_amount": self.loan1.max_amount,
                        "min_amount": self.loan1.min_amount,
                        "rate": self.loan1.rate,
                        "duration": self.loan1.duration,
                    }
                ),
                OrderedDict(
                    {
                        "id": self.loan2.id,
                        "max_amount": self.loan2.max_amount,
                        "min_amount": self.loan2.min_amount,
                        "rate": self.loan2.rate,
                        "duration": self.loan2.duration,
                    }
                ),
            ],
        )

    def test_get_customerLoan_with_amount(self):
        data = {"amount": 7000}
        response = self.client.get(self.customer_loan_url, data, format="json")

        self.assertEqual(
            response.data["results"][0],
            OrderedDict(
                {
                    "id": self.loan2.id,
                    "max_amount": self.loan2.max_amount,
                    "min_amount": self.loan2.min_amount,
                    "rate": self.loan2.rate,
                    "duration": self.loan2.duration,
                }
            ),
        )

    def test_get_customerLoan_amount_not_within_loan_range(self):
        data = {"amount": 500}
        response = self.client.get(self.customer_loan_url, data, format="json")
        self.assertEqual(response.data["results"], [])


class AmortizationViewSetTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="ahmed", user_type="customer")
        user.set_password("123456")
        user.save()

        data = {"username": "ahmed", "password": "123456"}
        self.loan1 = Loan.objects.create(
            max_amount=2000, min_amount=1000, rate=20, duration=1
        )
        response = self.client.post("/api/token/", data, format="json")
        self.token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.loan1 = CustomerLoan.objects.create(
            customer=user, loan=self.loan1, amount=1500
        )

        self.amortization_detail_url = reverse('loans:amortization-detail', kwargs={'pk':1})
        self.amortization_list_url = reverse('loans:amortization-list')


    def test_get_customer_loans(self):
        response = self.client.get(self.amortization_list_url, format="json")
        self.assertEqual(response.json()["results"], [{"id": 1, "amount": 1500}])

    def test_post_amortrization_table(self):
        response = self.client.get(self.amortization_detail_url, format="json")
        installment_dates = get_same_day_from_next_months(
            months_number=self.loan1.loan.duration * 12,
            start_date=self.loan1.created_at,
        )
        installments = {}

        for installment_date in installment_dates:
            installments[installment_date] = 150.0

        self.assertEqual(response.json(), installments)
