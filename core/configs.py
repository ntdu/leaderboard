import functools
from pathlib import Path

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    DB_MASTER_ENABLE: bool = True
    DB_MASTER_ENGINE: str = "django.db.backends.postgresql"
    DB_MASTER_NAME: str
    DB_MASTER_USERNAME: str
    DB_MASTER_PASSWORD: str
    DB_MASTER_HOST: str
    DB_MASTER_PORT: str

    def get_databases(self):
        return {
            "default": {
                "ENGINE": self.DB_MASTER_ENGINE,
                "NAME": self.DB_MASTER_NAME,
                "USER": self.DB_MASTER_USERNAME,
                "PASSWORD": self.DB_MASTER_PASSWORD,
                "HOST": self.DB_MASTER_HOST,
                "PORT": self.DB_MASTER_PORT,
                "ATOMIC_REQUESTS": True,
                "CONN_MAX_AGE": 60,
                "CONN_HEALTH_CHECKS": True,
            }
        }


class CelerySettings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_ACKS_LATE: bool = True
    CELERY_TASK_DEFAULT_PRIORITY: int = 5
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = 1
    CELERY_WORKER_CONCURRENCY: int = 1


class KafkaSettings(BaseSettings):
    KAFKA_HOST: str = 'localhost'
    KAFKA_PORT: int = 9092
    KAFKA_USER: str = None
    KAFKA_AUTH: str = None

    def get_kafka_url(self) -> str:
        return f'{self.KAFKA_HOST}:{self.KAFKA_PORT}'


class Configs(CelerySettings, KafkaSettings, DatabaseSettings, BaseSettings):
    DEBUG: bool = False
    ENVIRONMENT: str = "dev"
    HOST: str = "localhost"
    PORT: int = "8000"

    SECRET_KEY: str
    ALLOWED_HOSTS: list = []
    INTERNAL_IPS: list = ["127.0.0.1"]

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"


@functools.lru_cache(maxsize=1)
def get_configs() -> Configs:
    return Configs()
