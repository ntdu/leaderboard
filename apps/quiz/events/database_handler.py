
import time
import logging
from threading import Timer
from kafka import KafkaTopic

from .enumerations import AbstractEventHandler
from quiz.models import UserQuiz, UserAnswer
from .utils import TimerManager

logger = logging.getLogger(__name__)


class DatabaseHandler(AbstractEventHandler):
    handlers = {
        KafkaTopic.QUIZ_ANSWER: 'answer_quiz',
        KafkaTopic.QUIZ_JOIN: 'join_quiz'
    }
    
    def __init__(self, kafka_topic, batch_size=50, interval=0.5):
        self.topic = kafka_topic
        self.batch_size = batch_size

        self.user_answers = []

        self.callback = None
        self.interval = interval
        self.timer_manager = TimerManager(interval, self.check_and_save)

    def _get_handler(self):
        handler_name = DatabaseHandler.handlers.get(self.topic)
        if not handler_name:
            raise ValueError(f"Error: No handler for event type: {self.topic} in RedisHandler")
        return getattr(self, handler_name)

    def process(self, event, callback):
        self.callback = callback
        handler = self._get_handler()
        return handler(event)

    def answer_quiz(self, event):
        self.add_user_answer(event)  # 204 transactions

        if len(self.user_answers) >= self.batch_size:
            self._save_user_answers()

        self.timer_manager.start_or_reset_timer()
        return False

    def check_and_save(self):
        if self.user_answers:
            self._save_user_answers()

    def stop(self):
        self.timer_manager.stop_timer()

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

    def _save_user_answers(self):
        logger.info(f"save_user_answers: {len(self.user_answers)}")
        if self.user_answers:
            UserAnswer.objects.bulk_create(self.user_answers)
            self.user_answers = []

            if self.callback:
                self.callback()
