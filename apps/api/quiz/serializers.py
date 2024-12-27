import logging
from rest_framework import serializers

from quiz.models import UserQuiz, UserAnswer


logger = logging.getLogger(__name__)


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer()
        fields = ['user', 'question', 'answer']

    def create(self, validated_data):
        # TODO: Validate input data using Redis
        # Push validated data to Kafka
        return UserAnswer.objects.create(**validated_data)
