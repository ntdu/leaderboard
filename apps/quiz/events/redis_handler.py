
import time
import json
import random
import logging

from redis import Redis
from kafka import KafkaTopic
from django_redis import get_redis_connection
from .enumerations import AbstractEventHandler, QuizKeys
from .utils import TimerManager


logger = logging.getLogger(__name__)
redis_client: Redis = get_redis_connection()


class RedisHandler(AbstractEventHandler):
    handlers = {
        KafkaTopic.QUIZ_ANSWER: 'answer_quiz',
        KafkaTopic.QUIZ_JOIN: 'join_quiz',
        KafkaTopic.LEADERBOARD_CHANGES: 'learboard_changes',
        KafkaTopic.LEADERBOARD_UPDATES: 'learboard_updates'
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
        sorted_set_key = QuizKeys.QUIZ_LEADERBOARD.value.format(event['quiz_id'])
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
        question_key = QuizKeys.QUIZ_QUESTION.value.format(quiz_id)

        correct_answer = redis_client.hget(question_key, QuizKeys.QUIZ_CORRECT_ANSWER.value.format(question_id))
        score = int(redis_client.hget(question_key, QuizKeys.QUIZ_QUESTION_SCORE.value.format(question_id)))
    
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

    def learboard_changes(self, event):
        # event = {
        #     'quiz_id': event['quiz_id'],
        #     'timestamp': int(time.time())
        # }

        quiz_id = event['quiz_id']
        timestamp = event['timestamp']

        quiz_last_changes_key = QuizKeys.QUIZ_LAST_CHANGES.value.format(quiz_id)
        last_changes = redis_client.get(quiz_last_changes_key)

        if not last_changes:
            redis_client.set(quiz_last_changes_key, timestamp)
        else:
            last_changes = int(last_changes)
            if timestamp - last_changes < 0.5:
                logger.info(f"Skipping Redis leaderboard_changes event for quiz {quiz_id} at {timestamp}")
                return True

        sorted_set_key = QuizKeys.QUIZ_LEADERBOARD.value.format(event['quiz_id'])

        # Get all users
        all_users = redis_client.zrevrange(sorted_set_key, 0, -1, withscores=True)
        logger.info(f"Redis leaderboard_changes event for quiz {quiz_id} at {timestamp}")
        logger.info(f"All users in quiz {quiz_id} at {timestamp}: {all_users}")

        # Send the leaderboard updates
        return False
