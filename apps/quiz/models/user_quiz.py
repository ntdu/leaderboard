__all__ = [
    'UserQuiz',
    'UserAnswer',
]

from django.db import models
from django.conf import settings

from .base import AbstractBaseModel
from .quiz import Quiz, Question

class UserQuiz(AbstractBaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_quizs')


class UserAnswer(AbstractBaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_answers')
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
