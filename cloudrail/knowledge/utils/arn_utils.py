import functools
import logging
import re
from typing import Optional, Tuple
from arnparse import arnparse
from botocore.utils import InvalidArnException, ArnParser


@functools.lru_cache(maxsize=None)
def are_arns_intersected(resource_arn: str, target_arn: str):
    try:
        if resource_arn == '*' or target_arn == '*':
            return True
        elif (not is_valid_arn(resource_arn) and is_valid_arn(target_arn)) or (is_valid_arn(resource_arn) and not is_valid_arn(target_arn)):
            return False

        resource_arn_parsed = arnparse(resource_arn) if is_valid_arn(resource_arn) else DummyArnObject(resource_arn)
        target_arn_parsed = arnparse(target_arn) if is_valid_arn(resource_arn) else DummyArnObject(target_arn)

        arn_length = _get_arn_by_length(resource_arn_parsed, target_arn_parsed)
        long_arn = arn_length[0]
        short_arn = arn_length[1]

        for attribute, value in vars(short_arn).items():
            if not hasattr(long_arn, attribute):
                return False

            target_attribute = long_arn.__getattribute__(attribute)
            if not value or '*' in value or not target_attribute or '*' in target_attribute:  # wildcards
                continue

            pattern = re.compile(value.replace('*', '.*', -1))
            if not pattern.fullmatch(target_attribute):
                return False
    except IndexError:  # This happens when the user put an illegal ARN in a policy principal/resource (for example, arn:aws:sqs:*)
        return False

    return True


def _get_arn_by_length(first_arn: object, second_arn: object) -> Tuple:
    if len(first_arn.__dict__.values()) >= len(second_arn.__dict__.values()):
        return (first_arn, second_arn)
    else:
        return (second_arn, first_arn)

@functools.lru_cache(maxsize=None)
def is_arn_contained_in_arn(contained: str, container: str):
    if container == '*':
        return True
    if contained == '*' or not (is_valid_arn(contained) and is_valid_arn(container)):
        return False

    contained = contained.replace(':instance-profile/', ':role/')
    container = container.replace(':instance-profile/', ':role/')

    resource_arn_parsed = arnparse(contained)
    target_arn_parsed = arnparse(container)

    for attribute, value in vars(resource_arn_parsed).items():
        if not hasattr(target_arn_parsed, attribute):
            return False

        target_value = target_arn_parsed.__getattribute__(attribute)

        if (target_value == '*' or not target_value or target_value == value) or \
                (attribute == "resource" and target_value == "root"):
            continue

        return False

    return True


def get_arn_resource(arn: str):
    if arn and arn.startswith('arn'):
        return arnparse(arn).resource
    return arn


def get_arn_region(arn: str):
    if arn and arn.startswith('arn'):
        return arnparse(arn).region
    return arn


def get_arn_account_id(arn: str):
    if arn and arn.startswith('arn'):
        return arnparse(arn).account_id
    return arn


def build_arn(service: str, region: Optional[str], account_id: Optional[str],
              resource_type: Optional[str], path: Optional[str], resource_name: str) -> str:
    region = region or ''
    account_id = account_id or ''
    if service in ['s3', 'sns', 'apigateway', 'execute-api']:
        resource = resource_name
    elif service == 'db' or resource_type == 'destination':
        resource = f"{resource_type}:{resource_name}"
    else:
        resource = f"{resource_type}{path or '/'}{resource_name}"

    return f"arn:aws:{service}:{region}:{account_id}:{resource}"


@functools.lru_cache(maxsize=None)
def is_valid_arn(arn: str) -> bool:
    try:
        parser: ArnParser = ArnParser()
        parser.parse_arn(arn)
        return True
    except InvalidArnException:
        return False
    except Exception:
        logging.warning(f'failed parse arn {arn}')
        return False

class DummyArnObject:
    def __init__(self, arn_str: str):
        splitted_arn = arn_str.split(':')
        for item in splitted_arn:
            if '/' in item:
                split_slash = item.split('/')
                for item_split in split_slash:
                    setattr(self, item_split, item_split)
            else:
                setattr(self, item, item)
