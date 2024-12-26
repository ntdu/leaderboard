
import logging
from kafka import KafkaTopic
from .enumerations import AbstractEventHandler


logger = logging.getLogger(__name__)


class DatabaseHandler(AbstractEventHandler):
    handlers = {
        KafkaTopic.QUIZ_ANSWER: 'answer_quiz',
        KafkaTopic.QUIZ_JOIN: 'join_quiz'
    }

    def get_handler(self):
        handler_name = DatabaseHandler.handlers.get(self.topic)
        if not handler_name:
            raise ValueError(f"Error: No handler for event type: {self.topic} in RedisHandler")
        return getattr(self, handler_name)

    def process(self, event):
        handler = self.get_handler()
        return handler(event)

    @staticmethod
    def answer_quiz(event):
        logger.info("Database answer_quiz event")
        logger.info("=" * 100)
        # Implement the logic for answering a quiz
        pass

    @staticmethod
    def join_quiz(event):
        # Implement the logic for joining a quiz
        pass