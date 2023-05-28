
from loans.views import LoanViewSet, CustomerLoanViewSet, AmortizationViewSet
from rest_framework import routers

app_name = "loans"

router = routers.DefaultRouter()


router.register(r"customerLoans", CustomerLoanViewSet, basename="custmer-loan")
router.register(r"amortization", AmortizationViewSet, basename="amortization")
router.register(r"", LoanViewSet)

urlpatterns = router.urls
