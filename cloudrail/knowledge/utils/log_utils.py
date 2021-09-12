import logging
from datetime import datetime


def log_execution_time(function):
    def wrapper(*args, **attributes):
        start_time = datetime.now()
        result = function(*args, **attributes)
        end_time = datetime.now()
        logging.info(f'execution duration of {function.__name__} was {end_time - start_time} seconds')
        return result

    return wrapper
