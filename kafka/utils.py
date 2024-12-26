
import logging
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

logger = logging.getLogger(__name__)

def create_kafka_topics(broker, topics):
    admin_client = AdminClient({'bootstrap.servers': broker})

    # Get the list of existing topics
    existing_topics = admin_client.list_topics(timeout=10).topics

    # Filter out topics that already exist
    new_topics = [NewTopic(topic.value, num_partitions=1, replication_factor=1) for topic in topics if topic.value not in existing_topics]

    if not new_topics:
        logger.info("All topics already exist.")
        return

    fs = admin_client.create_topics(new_topics)

    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            logger.info(f"Topic {topic} created")
        except KafkaException as e:
            logger.exception(f"Failed to create topic {topic}: {e}")
