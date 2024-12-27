from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.api.handlers import CustomJSONRenderer
from quiz.models import UserQuiz, UserAnswer
from .serializers import UserAnswerSerializer


@extend_schema(tags=["User Answer"])
class UserAnswerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    renderer_classes = (CustomJSONRenderer,)
