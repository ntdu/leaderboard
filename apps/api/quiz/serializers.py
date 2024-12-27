import logging
from rest_framework import serializers

from quiz.models import UserQuiz, UserAnswer


logger = logging.getLogger(__name__)


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer()
        fields = ['user', 'question', 'answer']

    def create(self, validated_data):
        return UserAnswer.objects.create(**validated_data)
