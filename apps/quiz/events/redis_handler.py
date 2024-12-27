
import logging


from kafka import KafkaTopic
from django_redis import get_redis_connection
from .enumerations import AbstractEventHandler
from .utils import TimerManager


logger = logging.getLogger(__name__)
redis_client = get_redis_connection()


class RedisHandler(AbstractEventHandler):
    handlers = {
        KafkaTopic.QUIZ_ANSWER: 'answer_quiz',
        KafkaTopic.QUIZ_JOIN: 'join_quiz',
        KafkaTopic.LEADERBOARD_CHANGES: 'learboard_updates',
        KafkaTopic.LEADERBOARD_UPDATES: 'learboard_changes'
    }

    def __init__(self, kafka_topic, batch_size=50, interval=0.5):
        self.topic = kafka_topic
        self.batch_size = batch_size

        self.user_answers = []

        self.callback = None
        self.interval = interval
        self.timer_manager = TimerManager(interval, self.check_and_save)

    def _get_handler(self):
        handler_name = RedisHandler.handlers.get(self.topic)
        if not handler_name:
            raise ValueError(f"Error: No handler for event type: {self.topic} in RedisHandler")
        return getattr(self, handler_name)

    def process(self, event, callback):
        self.callback = callback
        handler = self._get_handler()
        return handler(event)

    def answer_quiz(self, event):
        logger.info("Redis answer_quiz event")
        user_score = self._calculate_score(event['quiz_id'], event['question_id'], event['answer'])
        logger.info(f"{user_score=}")
        # Implement the logic for answering a quiz
        return True

    def _calculate_score(self, quiz_id, question_id, answer):
        question_key = f'quiz__{quiz_id}__questions'
        correct_answer = redis_client.hget(question_key, f'question_{question_id}_correct_answer')
        score = int(redis_client.hget(question_key, f'question_{question_id}_score'))
    
        if correct_answer == answer:
            return score
        return 0

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

    @staticmethod
    def learboard_updates(event):
        # Implement the logic for joining a quiz
        pass

    @staticmethod
    def learboard_changes(event):
        # Implement the logic for joining a quiz
        pass