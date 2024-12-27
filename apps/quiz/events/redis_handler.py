
import logging


from kafka import KafkaTopic
from .enumerations import AbstractEventHandler
from .utils import TimerManager


logger = logging.getLogger(__name__)


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
        # Implement the logic for answering a quiz
        return True

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