import base64
import json
import random
import string
import sys
import zlib
from typing import Optional, List
import jsonpickle
import yaml
from cfn_tools import load_yaml
from cloudrail.knowledge.utils.log_utils import log_execution_time


class StringUtils:
    @staticmethod
    def convert_enum_to_title(value):
        known_acronyms = {'Iam'}
        value_with_space = value.replace('_', ' ')
        if value.upper() == value:
            value_as_title = value_with_space.upper()
        else:
            value_as_title = value_with_space.title()
        if value_as_title in known_acronyms:
            return value_as_title.upper()
        else:
            return value_as_title

    @staticmethod
    def convert_strs_to_bool(values: List[str]) -> Optional[bool]:
        if not values:
            return None
        found_true = False
        found_false = False
        for value in values:
            if value and value.lower() == 'true':
                found_true = True
            if value and value.lower() == 'false':
                found_false = True
        if found_false and found_true:
            return None
        if found_true:
            return True
        if found_false:
            return False
        return None

    @staticmethod
    def convert_to_bool(value: Optional[str]) -> Optional[bool]:
        if not value:
            return None
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        return None

    @staticmethod
    def clean_markdown(value: str) -> Optional[str]:
        if not value:
            return None
        return value.replace('<', '').replace('>', '')

    @staticmethod
    @log_execution_time
    def compress_text(text, pickle_it: bool = True):
        if text is None:
            return text
        if pickle_it:
            sys.setrecursionlimit(100000)
            text = jsonpickle.encode(text)
        text = zlib.compress(text.encode())
        text = base64.b64encode(text).decode()
        return text

    @staticmethod
    @log_execution_time
    def decompress_text(text, unpickle_it: bool = True):
        if text is None:
            return text
        text = base64.b64decode(text)
        text = zlib.decompress(text).decode()
        if unpickle_it:
            sys.setrecursionlimit(100000)
            text = jsonpickle.decode(text)
        return text

    @classmethod
    def dict_deep_update(cls, source: dict, target: dict) -> None:
        for key, value in target.items():  # todo - remove to appropriate class
            if key in source:
                if isinstance(value, dict):
                    cls.dict_deep_update(source.get(key), value)
                elif isinstance(value, list):
                    # todo - support list of dict
                    source_set: set = set(source.get(key, set()))
                    target_set: set = set(value)
                    diff_sets: set = source_set - target_set
                    source_set.update(diff_sets)
                else:
                    source[key] = value
            else:
                source[key] = value

    @staticmethod
    def is_json(text: str) -> bool:
        try:
            json.loads(text)
            return True
        except Exception:
            return False

    @staticmethod
    def is_yaml(text: str) -> bool:
        try:
            yaml.safe_load(text)
            return True
        except Exception:
            try:
                load_yaml(text)
                return True
            except Exception:
                return False


def generate_random_string() -> str:
    return ''.join((random.choice(string.ascii_lowercase) for _ in range(10)))
