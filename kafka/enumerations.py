
import enum

@enum.unique
class KafkaConsumerGroup(enum.Enum):
    """
    Enumerations for Kafka Consumer Group
    """

    DB_QUIZ_ANSWER_CONSUMER = 'db-quiz-answer-consumer'
    REDIS_QUIZ_ANSWER_CONSUMER = 'redis-quiz-answer-consumer'


@enum.unique
class KafkaTopic(enum.Enum):
    """
    Enumerations for Kafka Consumer Group
    """

    QUIZ_ANSWER = 'quiz_answer_queue'
    QUIZ_JOIN = 'quiz_join_queue'
    LEADERBOARD_CHANGES = 'leaderboard_changes_queue'
    LEADERBOARD_UPDATES = 'leaderboard_updates_queue'
