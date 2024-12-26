
from django.core.management.base import BaseCommand

from kafka import KafkaTopic
from quiz.events.event_factory import EventHandlerFactory
from quiz.events.enumerations import EventHandlerType

from quiz.event_engine import EventsEngine
from core.configs import get_configs


configs = get_configs()


class Command(BaseCommand):
    help = 'Start the Kafka consumer'

    def handle(self, *args, **kwargs):
        event_handler = EventHandlerFactory(EventHandlerType.REDIS, KafkaTopic.QUIZ_ANSWER).create_handler()

        event_engine = EventsEngine(KafkaTopic.QUIZ_ANSWER, event_handler)
        event_engine.start()
        event_engine.consume()
