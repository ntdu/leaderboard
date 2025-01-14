
import json
import logging

from core.kafka import get_kafka_consumer, get_kafka_producer
from utils.decorators import retry_on_exception

from .events.enumerations import AbstractEventHandler


logger = logging.getLogger(__name__)


RETRY_TOPIC = "jobs-retry"


class EventsEngine:
    def __init__(self, *topic: str, group_id: str, event_handlers: AbstractEventHandler):
        # self.consumer = get_kafka_consumer(topic, RETRY_TOPIC) # Add retry topic later
        self.group_id = group_id
        self.consumer = get_kafka_consumer(*topic, group_id=group_id)
        self.producer = get_kafka_producer()

        self.running = False
        self.event_handlers = event_handlers
        self.event_handlers.set_producer(self.producer)

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
        logger.info(f"Received message: {event_dict} in {self.group_id}")

        is_finish = self.event_handlers.process(event_dict, self.commit_message)
        if is_finish:
            self.commit_message()

    def commit_message(self):
        logger.info(f"{self.group_id=} Committing message")
        logger.info("")
        self.consumer.commit()

    def health_check(self) -> bool:
        return self.running
