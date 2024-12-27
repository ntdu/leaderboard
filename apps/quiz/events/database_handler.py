
import time
import logging
from threading import Timer
from kafka import KafkaTopic

from .enumerations import AbstractEventHandler
from quiz.models import UserQuiz, UserAnswer


logger = logging.getLogger(__name__)


class DatabaseHandler(AbstractEventHandler):
    handlers = {
        KafkaTopic.QUIZ_ANSWER: 'answer_quiz',
        KafkaTopic.QUIZ_JOIN: 'join_quiz'
    }
    
    def __init__(self, kafka_topic, batch_size=100, interval=10):
        self.topic = kafka_topic
        self.batch_size = batch_size
        self.interval = interval
        self.last_message_time = time.time()

        self.user_answers = []
        self.timer = None

    def get_handler(self):
        handler_name = DatabaseHandler.handlers.get(self.topic)
        if not handler_name:
            raise ValueError(f"Error: No handler for event type: {self.topic} in RedisHandler")
        return getattr(self, handler_name)

    def process(self, event):
        handler = self.get_handler()
        return handler(event)

    def answer_quiz(self, event):
        self.add_user_answer(event)
        self.last_message_time = time.time()

        print(f"User answers: {len(self.user_answers)=}")
        if len(self.user_answers) >= self.batch_size:
            self.save_user_answers()
        else:
            self.start_or_reset_timer()

        return False

    def start_or_reset_timer(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(self.interval, self.check_and_save)
        self.timer.start()

    def check_and_save(self):
        current_time = time.time()
        if self.user_answers and (current_time - self.last_message_time >= self.interval):
            self.save_user_answers()
        self.timer = Timer(self.interval, self.check_and_save)
        self.timer.start()

    def stop(self):
        self.stop_timer()

    def stop_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

    @staticmethod
    def join_quiz(event):
        # Implement the logic for joining a quiz
        pass

    def add_user_answer(self, event):
        user_answer = UserAnswer(
            user_id=event['user_id'],
            question_id=event['question_id'],
            answer=event['answer']
        )
        self.user_answers.append(user_answer)

    def save_user_answers(self):
        print(f"save_user_answers: {len(self.user_answers)=}")
        if self.user_answers:
            UserAnswer.objects.bulk_create(self.user_answers)
            self.user_answers = []
