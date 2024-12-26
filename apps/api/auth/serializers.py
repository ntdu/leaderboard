import logging
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


logger = logging.getLogger(__name__)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_name'] = user.user_name
        token['email'] = user.email

        return token

    def validate(self, attrs):
        credentials = {
            'password': attrs.get('password'),
            'user_name': attrs.get('user_name')
        }

        user = None
        if credentials['user_name']:
            user = get_user_model().objects.filter(user_name=credentials['user_name']).first()

        if not user:
            user = get_user_model().objects.filter(email=credentials['user_name']).first()

        if user and user.check_password(credentials['password']):
            refresh = self.get_token(user)

            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_name': user.user_name,
                'email': user.email,
            }

            return data
        else:
            raise serializers.ValidationError('No active account found with the given credentials')

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
