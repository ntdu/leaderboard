
import logging
from confluent_kafka import Producer


logger = logging.getLogger(__name__)


class KafkaProducer:
    # Just for testing purpose
    def __init__(self, base_url):
        self.producer = Producer({
            'bootstrap.servers': base_url,
        })

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def produce(self, topic, key, value):
        try:
            self.producer.produce(topic, key=key, value=value, callback=self.delivery_report)
            self.producer.poll(0)
        except Exception as e:
            logger.error(f"Failed to produce message: {e}")

    def flush(self):
        self.producer.flush()
