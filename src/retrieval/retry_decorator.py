import time
import functools
import logging

def retry(tries=3, delay=5, backoff=2):
    """A simple retry decorator."""
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.warning(f"Error calling {func.__name__}: {e}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper_retry
    return decorator_retry
