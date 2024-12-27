
import logging
from confluent_kafka import Consumer


logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, base_url: str, username: str, password: str, topics: list[str], group_id: str):
        logger.info(f"KafkaConsumer Init {base_url=} {username=} {password=} {topics=} {group_id=}")
        config = {
            'bootstrap.servers': base_url,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,
            'partition.assignment.strategy': 'roundrobin',
        }

        if username and password:
            config.update({
                'security.protocol': 'SASL_PLAINTEXT',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': username,
                'sasl.password': password,
            })

        self.consumer = Consumer(config)
        self.topics = topics

    def start(self):
        self.consumer.subscribe(self.topics)

    def stop(self):
        self.consumer.close()

    def consume(self):
        try:
            while True:
                message = self.consumer.poll(timeout=1.0)
                if message is None:
                    continue

                if message.error():
                    logger.error(f"Kafka error: {message.error()}")
                    continue

                yield message.value().decode('utf-8')

        except KeyboardInterrupt:
            logger.info("Kafka consumer interrupted by user.")
        except Exception as e:
            logger.error(f"Kafka consumer Unexpected error: {e}")
        finally:
            self.stop()

    def commit(self):
        self.consumer.commit()

