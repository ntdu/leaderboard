
import json
import random
from redis import Redis
from django.core.management.base import BaseCommand

from kafka import KafkaTopic, KafkaConsumerGroup
from core.kafka import KafkaProducer

from quiz.models import UserQuiz, UserAnswer, Quiz, Question
from django.contrib.auth import get_user_model
from django_redis import get_redis_connection


redis_client: Redis = get_redis_connection()


class Command(BaseCommand):
    help = 'Seed the database with comments'

    def init_data(self):
        user1 = get_user_model().objects.all().first()
        if not user1:
            user1 = get_user_model().objects.create_user(
                email='testuser@example.com',
                user_name='testuser',
                password='testpassword123'
            )

        user2 = get_user_model().objects.all().exclude(id=user1.id).first()
        if not user2:
            user2 = get_user_model().objects.create_user(
                email='testuser1@example.com',
                user_name='testuser1',
                password='testpassword123'
            )

        quiz = Quiz.objects.all().last()
        if not quiz:
            quiz = Quiz.objects.create(
                title='Test Quiz',
                description='Test Quiz Description',
                available_at='2024-12-26', expires_at='2025-01-02')

            Question.objects.create(
                quiz=quiz,
                question_id=1,
                text='Test Question 1',
                answer_choices=json.dumps(['A', 'B', 'C', 'D']),
                correct_answer='A',
                score=10
            )

            Question.objects.create(
                quiz=quiz,
                question_id=2,
                text='Test Question 2',
                answer_choices=json.dumps(['A', 'B', 'C', 'D']),
                correct_answer='B',
                score=10
            )

        user_quiz = UserQuiz.objects.filter(quiz=quiz, user=user1).first()
        if not user_quiz:
            UserQuiz.objects.create(quiz=quiz, user=user1)

        user_quiz = UserQuiz.objects.filter(quiz=quiz, user=user2).first()
        if not user_quiz:
            UserQuiz.objects.create(quiz=quiz, user=user2)

    def init_redis(self):
        quiz = Quiz.objects.all().last()

        question_1 = Question.objects.filter(quiz=quiz, question_id=1).values(
            'question_id', 'correct_answer', 'score'
        ).first()
        question_2 = Question.objects.filter(quiz=quiz, question_id=2).values(
            'question_id', 'correct_answer', 'score'
        ).first()

        print(f'{question_1=}')
        print(f'{question_2=}')
        if question_1:
            print(f'quiz__{quiz.id}__questions')
            redis_client.hset(f'quiz__{quiz.id}__questions', mapping={
                f'question_{question_1["question_id"]}_correct_answer': question_1['correct_answer'],
                f'question_{question_1["question_id"]}_score': question_1['score']
            })

        if question_2:
            redis_client.hset(f'quiz__{quiz.id}__questions', mapping={
                f'question_{question_2["question_id"]}_correct_answer': question_2['correct_answer'],
                f'question_{question_2["question_id"]}_score': question_2['score']
            })

    def handle(self, *args, **kwargs):
        self.init_data()
        self.init_redis()
        producer = KafkaProducer('localhost:9092')

        print(redis_client.get('cache_key'))
        print(Question.objects.count())
        print(Question.objects.last().quiz)
        print(Question.objects.last().question_id)
        print(Question.objects.all())

        user1 = get_user_model().objects.all().first()
        user2 = get_user_model().objects.all().exclude(id=user1.id).first()

        user1_quiz = UserQuiz.objects.filter(user=user1).first()
        quiz = Quiz.objects.filter(id=user1_quiz.quiz.id).first()

        user2_quiz = UserQuiz.objects.filter(user=user2).first()
        quiz2 = Quiz.objects.filter(id=user2_quiz.quiz.id).first()
        for i in range(1, 10):
            validated_data = {
                "quiz_id": str(quiz.id),
                "question_id": 1,
                "user_id": user1.id,
                "answer": 'A',
            }
            producer.produce(KafkaTopic.QUIZ_ANSWER.value, key=str(random.randint(0, 1000000)), value=json.dumps(validated_data))
            producer.flush()

            validated_data = {
                "quiz_id": str(quiz2.id),
                "question_id": 1,
                "user_id": user2.id,
                "answer": 'A',
            }
            producer.produce(KafkaTopic.QUIZ_ANSWER.value, key=str(random.randint(0, 1000000)), value=json.dumps(validated_data))
            producer.flush()

            # producer.produce(KafkaTopic.QUIZ_ANSWER.value, key=str(random.randint(0, 1000000)), value=json.dumps(validated_data))
            # producer.flush()

            # producer.produce(KafkaTopic.QUIZ_ANSWER.value, key=str(random.randint(0, 1000000)), value=json.dumps(validated_data))
            # producer.flush()

        self.stdout.write(self.style.SUCCESS(F'Successfully seeded answers into the database'))
