
from core.configs import get_configs

configs = get_configs()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            '()': "pythonjsonlogger.jsonlogger.JsonFormatter",
            'format': '%(levelname)s %(asctime)s %(msecs)d %(processName)s %(process)d %(threadName)s %(pathname)s %(funcName)s %(lineno)d %(message)s'
        },
        'local': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': configs.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'local' if configs.ENVIRONMENT == 'local' else 'standard',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
