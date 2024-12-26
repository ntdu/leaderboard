
__all__ = ['EventHandlerFactory']

import logging

from kafka import KafkaTopic
from .enumerations import EventHandlerType
from .redis_handler import RedisHandler
from .database_handler import DatabaseHandler


logger = logging.getLogger(__name__)


class EventHandlerFactory:
    def __init__(self, handler_type: EventHandlerType, topic: KafkaTopic):
        self.handler_type = handler_type
        self.topic = topic

    def create_handler(self):
        if self.handler_type == EventHandlerType.REDIS:
            return RedisHandler(self.topic)
        elif self.handler_type == EventHandlerType.DATABASE:
            return DatabaseHandler(self.topic)
        else:
            raise ValueError(f"Invalid event type: {self.handler_type}")


event_data = {
    'id': 1,
    'name': 'quiz',
    'description': 'quiz description',
    'answer': '0',
}
event_handler = EventHandlerFactory(EventHandlerType.REDIS, KafkaTopic.QUIZ_ANSWER).create_handler()
event_handler.process(event_data)
