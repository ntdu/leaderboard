import logging
from functools import lru_cache
from kafka import KafkaConsumer, KafkaProducer, KafkaConsumerGroup

from core.configs import get_configs


configs = get_configs()
logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer(base_url=configs.get_kafka_url())


@lru_cache(maxsize=1)
def get_kafka_consumer(*topics: str, group_id: KafkaConsumerGroup) -> KafkaConsumer:
    consumer = KafkaConsumer(
        base_url=configs.get_kafka_url(), 
        username=configs.KAFKA_USER,
        password=configs.KAFKA_AUTH,
        topics=list(topics),
        group_id=group_id
    )
    consumer.rebalance_timeout_ms = 800000
    consumer.max_poll_interval_ms = 800000
    return consumer
