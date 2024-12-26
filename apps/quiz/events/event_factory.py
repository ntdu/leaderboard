
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
        logger.info(f"Creating event handler for {self.handler_type}")
        if self.handler_type == EventHandlerType.REDIS.value:
            return RedisHandler(self.topic)
        elif self.handler_type == EventHandlerType.DATABASE.value:
            return DatabaseHandler(self.topic)
        else:
            raise ValueError(f"Invalid event type: {self.handler_type}")
