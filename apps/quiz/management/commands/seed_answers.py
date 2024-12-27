
import json
from django.core.management.base import BaseCommand

from kafka import KafkaTopic, KafkaConsumerGroup
from core.kafka import KafkaProducer

class Command(BaseCommand):
    help = 'Seed the database with comments'

    def handle(self, *args, **kwargs):
        producer = KafkaProducer()

        for i in range(1, 60):
            test_data = {
                "id": i,
            }
            producer.produce(KafkaTopic.QUIZ_ANSWER.value, key='0', value=json.dumps(test_data))
            producer.flush()

        self.stdout.write(self.style.SUCCESS(F'Successfully seeded comments into the database'))