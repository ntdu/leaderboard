
import json
from django.core.management.base import BaseCommand

from kafka import KafkaTopic, KafkaConsumerGroup
from core.kafka import KafkaProducer

from quiz.models import UserQuiz, UserAnswer, Quiz, Question
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Seed the database with comments'

    def init_data(self):
        user = get_user_model().objects.filter(id=1).first()
        if not user:
            user = get_user_model().objects.create_user(
                email='testuser@example.com',
                user_name='testuser',
                password='testpassword123'
            )

        quiz = Quiz.objects.filter(id=1).first()
        if not quiz:
            quiz = Quiz.objects.create(
                title='Test Quiz',
                description='Test Quiz Description',
                available_at='2024-12-26', expires_at='2025-01-02')

        question = Question.objects.filter(quiz=quiz, question_id=1).first()
        if not question:
            question = Question.objects.create(
                quiz=quiz,
                question_id=1,
                text='Test Question 1',
                answer_choices=json.dumps(['A', 'B', 'C', 'D']),
                correct_answer='A',
                score=10
            )

        question = Question.objects.filter(quiz=quiz, question_id=2).first()
        if not question:
            Question.objects.create(
                quiz=quiz,
                question_id=2,
                text='Test Question 2',
                answer_choices=json.dumps(['A', 'B', 'C', 'D']),
                correct_answer='B',
                score=10
            )

        user_quiz = UserQuiz.objects.filter(quiz=quiz, user=user).first()
        if not user_quiz:
            UserQuiz.objects.create(quiz=quiz, user=user)

    def handle(self, *args, **kwargs):
        self.init_data()
        producer = KafkaProducer()

        print(Question.objects.all())

        for i in range(1, 60):
            validated_data = {
                "question_id": 1,
                "user_id": 1,
                "answer": 'A',
            }
            producer.produce(KafkaTopic.QUIZ_ANSWER.value, key='0', value=json.dumps(validated_data))
            producer.flush()

        self.stdout.write(self.style.SUCCESS(F'Successfully seeded comments into the database'))
