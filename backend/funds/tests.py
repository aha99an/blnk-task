from rest_framework import status
from rest_framework.test import APITestCase
from funds.models import Fund, ProviderFund
from collections import OrderedDict
from users.models.user_model import User
from balance.models import Balance
from rest_framework.reverse import reverse


class FundsTests(APITestCase):
    def setUp(self):
        user = User.objects.create(username="ahmed", user_type="banker")
        user.set_password("123456")
        user.save()

        data = {"username": "ahmed", "password": "123456"}
        response = self.client.post("/api/token/", data, format="json")
        self.token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.funds_url = reverse("funds:fund-list")

    def test_create_fund(self):
        data = {"max_amount": 2000, "min_amount": 1000, "rate": 10, "duration": 10}
        response = self.client.post(self.funds_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Fund.objects.last().max_amount, 2000)
        self.assertEqual(Fund.objects.last().min_amount, 1000)
        self.assertEqual(Fund.objects.last().rate, 10)
        self.assertEqual(Fund.objects.last().duration, 10)
    
    def test_create_fund_min_amount_bigger_than_max_amount(self):
        data = {"max_amount": 1000, "min_amount": 2000, "rate": 10, "duration": 10}

        response = self.client.post(self.funds_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        
        self.assertEqual(response.json()["message"], "Sorry the minimum amount must be less than maximum amount")

    def test_get_fund(self):
        fund = Fund.objects.create(
            max_amount=2000, min_amount=1000, rate=10, duration=10
        )
        response = self.client.get(self.funds_url, format="json")
        fund.refresh_from_db()
        self.assertEqual(
            response.data["results"][0],
            OrderedDict(
                {
                    "id": fund.id,
                    "max_amount": fund.max_amount,
                    "min_amount": fund.min_amount,
                    "rate": fund.rate,
                    "duration": fund.duration,
                }
            ),
        )


class ProviderFundTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username="ahmed", user_type="provider")
        user.set_password("123456")
        user.save()

        data = {"username": "ahmed", "password": "123456"}
        response = self.client.post("/api/token/", data, format="json")
        self.token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.fund1 = Fund.objects.create(
            max_amount=2000, min_amount=1000, rate=10, duration=1
        )
        self.fund2 = Fund.objects.create(
            max_amount=10000, min_amount=5000, rate=20, duration=2
        )
        self.provider_fund_url = reverse("funds:provider_fund-list")

    def test_create_providerFund_within_range(self):
        fund = Fund.objects.create(
            max_amount=2000, min_amount=1000, rate=10, duration=1
        )

        data = {"fund": fund.pk, "amount": 1500}
        response = self.client.post(self.provider_fund_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()["message"],
            "Fund created successfully."
            + "Your fund with amount= "
            + "1500"
            + ", your returns= "
            + "150.0"
            + ", you will get "
            + "1650.0"
            + ", after "
            + "1"
            + " years.",
        )
        balance = Balance.objects.last()
        provider_fund = ProviderFund.objects.last()
        self.assertEqual(balance.balance, provider_fund.amount)

    def test_create_providerFund_with_notenough_amount(self):
        data = {"fund": 1, "amount": 500}
        response = self.client.post(self.provider_fund_url, data, format="json")
        self.assertEqual(
            response.json()["message"], "Error: please enter correct amount"
        )

    def test_get_providerFund(self):

        response = self.client.get(self.provider_fund_url, format="json")

        self.assertEqual(
            response.data["results"],
            [
                OrderedDict(
                    {
                        "id": self.fund1.id,
                        "max_amount": self.fund1.max_amount,
                        "min_amount": self.fund1.min_amount,
                        "rate": self.fund1.rate,
                        "duration": self.fund1.duration,
                    }
                ),
                OrderedDict(
                    {
                        "id": self.fund2.id,
                        "max_amount": self.fund2.max_amount,
                        "min_amount": self.fund2.min_amount,
                        "rate": self.fund2.rate,
                        "duration": self.fund2.duration,
                    }
                ),
            ],
        )

    def test_get_providerFund_with_amount(self):
        data = {"amount": 7000}
        response = self.client.get(self.provider_fund_url, data, format="json")

        self.assertEqual(
            response.data["results"][0],
            OrderedDict(
                {
                    "id": self.fund2.id,
                    "max_amount": self.fund2.max_amount,
                    "min_amount": self.fund2.min_amount,
                    "rate": self.fund2.rate,
                    "duration": self.fund2.duration,
                }
            ),
        )

    def test_get_providerFund_amount_not_within_fund_range(self):

        data = {"amount": 500}
        # here manually add amount to the months
        response = self.client.get(self.provider_fund_url, data, format="json")
        self.assertEqual(response.data["results"], [])
