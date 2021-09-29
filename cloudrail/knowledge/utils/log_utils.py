import json
import logging
from datetime import datetime

CLOUDRAIL_ERROR_STRING = '[CLOUDRAIL_ERROR]'


def log_execution_time(function):
    def wrapper(*args, **attributes):
        start_time = datetime.now()
        result = function(*args, **attributes)
        end_time = datetime.now()
        logging.info(f'execution duration of {function.__name__} was {end_time - start_time} seconds')
        return result

    return wrapper


def log_cloudrail_error(message: str, error_type: str):
    error = {'message': message,
             'type': error_type,
             'level': 10,
             'extra': {}}
    logging.error(f'{CLOUDRAIL_ERROR_STRING} {json.dumps(error)}')
