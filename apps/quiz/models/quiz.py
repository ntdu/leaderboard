
import uuid
from django.db import models
from django.conf import settings
from .base import AbstractBaseModel
 
 
class Quiz(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    available_at = models.DateTimeField()
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.title


class Question(AbstractBaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_id = models.IntegerField()
    text = models.TextField()
    answer_choices = models.JSONField()
    correct_answer = models.TextField()
    score = models.IntegerField()

    class Meta:
        unique_together = ["quiz", "question_id"]
