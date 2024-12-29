
import time
import json
import random
import logging

from redis import Redis
from kafka import KafkaTopic
from django_redis import get_redis_connection
from .enumerations import AbstractEventHandler
from .utils import TimerManager


logger = logging.getLogger(__name__)
redis_client: Redis = get_redis_connection()


class RedisHandler(AbstractEventHandler):
    handlers = {
        KafkaTopic.QUIZ_ANSWER: 'answer_quiz',
        KafkaTopic.QUIZ_JOIN: 'join_quiz',
        KafkaTopic.LEADERBOARD_CHANGES: 'learboard_updates',
        KafkaTopic.LEADERBOARD_UPDATES: 'learboard_changes'
    }

    def __init__(self, kafka_topic, batch_size=50, interval=0.5):
        self.topic = kafka_topic
        self.batch_size = batch_size
        self.producer = None

        self.user_answers = []

        self.callback = None
        self.interval = interval
        self.timer_manager = TimerManager(interval, self.check_and_save)

    def set_producer(self, producer):
        self.producer = producer

    def _get_handler(self):
        handler_name = RedisHandler.handlers.get(self.topic)
        if not handler_name:
            raise ValueError(f"Error: No handler for event type: {self.topic} in RedisHandler")
        return getattr(self, handler_name)

    def process(self, event, callback):
        self.callback = callback
        handler = self._get_handler()
        return handler(event)

    def answer_quiz(self, event):
        logger.info("Redis answer_quiz event")
        new_score = self._calculate_score(event['quiz_id'], event['question_id'], event['answer'])

        # Don't update the score if the answer is incorrect
        if new_score == 0:
            return False

        logger.info(f"{new_score=}")

        # Update user_score into sorted set
        sorted_set_key = f'quiz__{event["quiz_id"]}__scores'
        user_id = event['user_id']

        # Get the current score
        current_score = redis_client.zscore(sorted_set_key, user_id)
        if current_score is None:
            current_score = 0

        total_score = current_score + new_score

        # Update the sorted set with the new total score
        redis_client.zadd(sorted_set_key, {user_id: total_score})

        logger.info(f"Updated score for user {user_id} in quiz {event['quiz_id']}: {total_score}")

        self.producer.produce(KafkaTopic.LEADERBOARD_CHANGES.value, key=str(random.randint(0, 1000000)), value=json.dumps({
            'quiz_id': event['quiz_id'],
            'timestamp': int(time.time())
        }))
        self.producer.flush()
        return True

    def _calculate_score(self, quiz_id, question_id, answer):
        question_key = f'quiz__{quiz_id}__questions'
        correct_answer = redis_client.hget(question_key, f'question_{question_id}_correct_answer')
        score = int(redis_client.hget(question_key, f'question_{question_id}_score'))
    
        if correct_answer == answer:
            return score
        return 0

    def check_and_save(self):
        if self.user_answers:
            self._save_user_answers()

    def stop(self):
        self.timer_manager.stop_timer()

    def stop_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

    @staticmethod
    def join_quiz(event):
        # Implement the logic for joining a quiz
        pass

    @staticmethod
    def learboard_updates(event):
        # Implement the logic for joining a quiz
        pass

    @staticmethod
    def learboard_changes(event):
        # Implement the logic for joining a quiz
        pass