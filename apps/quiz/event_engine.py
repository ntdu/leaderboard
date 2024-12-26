
import json
import logging

from core.kafka import get_kafka_consumer
from utils.decorators import retry_on_exception

from .events.enumerations import AbstractEventHandler


logger = logging.getLogger(__name__)


RETRY_TOPIC = "jobs-retry"


class EventsEngine:
    def __init__(self, topic: str, event_handlers: AbstractEventHandler):
        # self.consumer = get_kafka_consumer(topic, RETRY_TOPIC) # Add retry topic later
        self.consumer = get_kafka_consumer(topic)
        self.producer = None

        self.running = False
        self.event_handlers = event_handlers

    def start(self):
        logger.info("Starting Events Engine...")
        self.consumer.start()
        self.running = True

        logger.info("Started Events Engine Successfully")

    def stop(self):
        logger.info("Stopping Events Engine...")
        self.running = False
        self.consumer.stop()

        logger.info("Stopped Events Engine Successfully")

    def consume(self):
        try:
            for message in self.consumer.consume():
                if not self.running:
                    break

                self.process_event(message)

        except KeyboardInterrupt:
            logger.info("Events engine interrupted by user.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.stop()

    @retry_on_exception(max_retries=3)
    def process_event(self, message):
        event_dict = json.loads(message)
        logger.info(f"Received message: {event_dict}")

        self.event_handlers.process(event_dict)

    def health_check(self) -> bool:
        return self.running
