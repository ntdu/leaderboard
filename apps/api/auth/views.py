from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView

from drf_spectacular.utils import extend_schema


from .serializers import MyTokenObtainPairSerializer, LogoutSerializer
from apps.api.handlers import CustomJSONRenderer


@extend_schema(tags=["Auth"])
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    renderer_classes = [CustomJSONRenderer]


@extend_schema(tags=["Auth"])
class TokenRefreshView(SimpleJWTTokenRefreshView):
    renderer_classes = [CustomJSONRenderer]


@extend_schema(tags=["Auth"])
class LogoutBlacklistTokenUpdateView(APIView):
    # TODO: Recheck this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer
    renderer_classes = [CustomJSONRenderer]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
