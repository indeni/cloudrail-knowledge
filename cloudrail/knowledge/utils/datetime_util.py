from datetime import datetime
import logging


def build_datetime(time_string, formatter):
    try:
        datetime_obj = datetime.strptime(time_string, formatter)
    except Exception as ex:
        message = f'Error while parse datetime for {time_string} string (should be in format: {formatter}). Message given: {ex}'
        logging.warning(message)
        datetime_obj = None

    return datetime_obj
