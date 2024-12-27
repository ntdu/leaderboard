import functools
from pathlib import Path
from typing import Optional

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


class RedisSettings(BaseSettings):
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_USER: Optional[str] = None
    REDIS_AUTH: Optional[str] = None

    def get_redis_url(self) -> str:
        if self.REDIS_USER and self.REDIS_AUTH:
            return f"redis://{self.REDIS_USER}:{self.REDIS_AUTH}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

        return f"redis://:{self.REDIS_AUTH}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class KafkaSettings(BaseSettings):
    KAFKA_HOST: str = 'localhost'
    KAFKA_PORT: int = 9092
    KAFKA_USER: Optional[str] = None
    KAFKA_AUTH: Optional[str] = None

    def get_kafka_url(self) -> str:
        return f'{self.KAFKA_HOST}:{self.KAFKA_PORT}'


class Configs(CelerySettings, RedisSettings, KafkaSettings, DatabaseSettings, BaseSettings):
    DEBUG: bool = False
    ENVIRONMENT: str = "dev"
    HOST: str = "localhost"
    PORT: int = "8000"

    LOG_LEVEL: Optional[str] = "DEBUG"

    SECRET_KEY: str
    ALLOWED_HOSTS: list = []
    INTERNAL_IPS: list = ["127.0.0.1"]

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"


@functools.lru_cache(maxsize=1)
def get_configs() -> Configs:
    return Configs()
