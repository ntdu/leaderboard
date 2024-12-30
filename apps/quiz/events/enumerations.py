
import enum
from abc import abstractmethod
from kafka import KafkaTopic
from typing import Optional, Callable


@enum.unique
class EventHandlerType(enum.Enum):
    """
    Enumerations for Event
    """

    NORMAL = 'normal'
    REDIS = 'redis'
    DATABASE = 'database'


class AbstractEventHandler:
    def __init__(self, topic: KafkaTopic):
        self.topic = topic

    @abstractmethod
    def process(self, event: dict, callback: Optional[Callable]) -> bool:
        pass

    @abstractmethod
    def set_producer(self, producer):
        pass


@enum.unique
class QuizKeys(enum.Enum):
    """
    Enumerations for Event
    """

    QUIZ_LEADERBOARD = 'quiz__{}__scores'
    QUIZ_QUESTION = 'quiz__{}__questions'
    QUIZ_LAST_CHANGES = 'quiz__{}__last_changes'
