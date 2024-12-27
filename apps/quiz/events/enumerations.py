
import enum
from abc import abstractmethod
from kafka import KafkaTopic

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
    def process(self, event: dict, callback: callable):
        pass
