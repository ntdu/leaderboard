
from django.core.management.base import BaseCommand

from kafka import KafkaTopic, KafkaConsumerGroup
from apps.quiz.events.event_factory import EventHandlerFactory
from quiz.events.enumerations import EventHandlerType

from quiz.event_engine import EventsEngine
from core.configs import get_configs


configs = get_configs()


class Command(BaseCommand):
    help = 'Start the leaderboard changes consumer'

    def handle(self, *args, **kwargs):
        event_handler = EventHandlerFactory(EventHandlerType.REDIS.value, KafkaTopic.LEADERBOARD_CHANGES).create_handler()

        event_engine = EventsEngine(
            KafkaTopic.LEADERBOARD_CHANGES.value,
            group_id=KafkaConsumerGroup.REDIS_QUIZ_ANSWER_CONSUMER,
            event_handlers=event_handler
        )
        event_engine.start()
        event_engine.consume()
