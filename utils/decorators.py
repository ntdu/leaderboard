
import logging
import functools
from django.db import close_old_connections, OperationalError


logger = logging.getLogger(__name__)


def retry_on_exception(max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    logger.error(f"Database connection error: {e}")
                    close_old_connections()

                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(f"Max retries reached for function: {func.__name__}")
                        raise
                except Exception as e:
                    logger.exception(f"Exception in function {func.__name__}", exc_info=e)
                    raise
        return wrapper
    return decorator