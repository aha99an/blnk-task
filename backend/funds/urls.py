from .views import FundViewSet, ProviderFundViewSet
from rest_framework import routers

app_name = "funds"

router = routers.DefaultRouter()

router.register(r"providerFund", ProviderFundViewSet, basename="provider_fund")
router.register(r"", FundViewSet, basename="fund")

urlpatterns = router.urls
