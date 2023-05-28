from rest_framework_simplejwt.views import TokenViewBase
from users.serializers import TokenObtainLifetimeSerializer


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainLifetimeSerializer
