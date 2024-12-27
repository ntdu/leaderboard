
from core.configs import get_configs

configs = get_configs()

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": configs.get_redis_url(),
        "OPTIONS": {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'decode_responses': True,
            },
        },
    }
}
