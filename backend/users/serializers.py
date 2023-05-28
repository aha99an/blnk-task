from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_type'] = self.user.user_type
        return data
