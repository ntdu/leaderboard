from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .serializers import RegistrationSerializer, UserSerializer
from apps.api.handlers import CustomJSONRenderer


@extend_schema(tags=["User"])
class RegistrationAPIView(generics.GenericAPIView):
    '''Registers user'''
    serializer_class = RegistrationSerializer
    renderer_classes = [CustomJSONRenderer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data['response'] = "Registration Successful!"
        refresh = RefreshToken.for_user(user=user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return Response(data, status.HTTP_201_CREATED)


@extend_schema(tags=["User"])
class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
