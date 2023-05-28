from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView
from users.views import TokenObtainPairView

router = routers.DefaultRouter()



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("funds/", include("funds.urls")),
    path("loans/", include("loans.urls")),
]
