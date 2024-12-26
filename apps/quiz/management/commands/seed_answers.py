
import json
from django.core.management.base import BaseCommand

from kafka import KafkaTopic, KafkaConsumerGroup
from core.kafka import KafkaProducer

class Command(BaseCommand):
    help = 'Seed the database with comments'

    def handle(self, *args, **kwargs):
        test_data = {
            "Addresses": [
                {
                "PSId": "00279277",
                "Email": "dunt14@fpt.com"
                },
                {
                "PSId": "00183946",
                "Email": "philk@fpt.com"
                }
            ],
            "MessageContent": {
                "modelCategory": "40",
                "sound": "sound_noti.mp3",
                "title": "Your Title",
                "message": "Short description or full message here",
                "priority": 5,
                "model": {
                    "LogId": "674d15b804237f2bd4df7d2c",
                    "Data": {
                        "Key1": "Value1",
                        "Key2": "Value2"
                    }
                }
            }
        }

        producer = KafkaProducer()
        producer.produce(KafkaTopic.QUIZ_ANSWER.value, key='0', value=json.dumps(test_data))
        producer.flush()

        self.stdout.write(self.style.SUCCESS(F'Successfully seeded comments into the database'))