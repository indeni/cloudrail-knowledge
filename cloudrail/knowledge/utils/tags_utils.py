from typing import Optional

from cloudrail.knowledge.utils.hash_utils import to_hashcode
from cloudrail.knowledge.utils.iac_fields_store import IacFieldsStore


def get_aws_tags(raw_aws_data: dict) -> Optional[dict]:
    salt = raw_aws_data.get('salt')
    possible_tag_keys = ['Tags', 'tags', 'TagSet']
    for tag_key in possible_tag_keys:
        if tag_key in raw_aws_data:
            tag_data = raw_aws_data[tag_key]
            if isinstance(tag_data, list):
                return _convert_aws_tags_to_dict(tag_data, salt)
            else:
                return _hash_tags_dict(tag_data, salt)
    return {}


def extract_name_from_tags(raw_data: dict) -> Optional[str]:
    tags = get_aws_tags(raw_data) or {}
    return tags.get('Name')


def _convert_aws_tags_to_dict(tags: list, salt: str) -> dict:
    result = {}
    for tag in tags:
        key = tag.get('Key') if tag.get('key') is None else tag.get('key')
        value = tag.get('Value') if tag.get('value') is None else tag.get('value')
        result[key] = value
    return _hash_tags_dict(result, salt) if salt else result


def _hash_tags_dict(dictionary: dict, salt: str) -> dict:
    allowed_tags = IacFieldsStore.get_terraform_aws_supported_services()['common'] \
        .known_fields.pass_values['tags'].known_fields.pass_values.keys()
    result = {}

    for key, value in dictionary.items():
        if key.lower() in allowed_tags:
            result[key] = value
        else:
            key_hashcode = f'{key}_hashcode'
            value_hashcode = to_hashcode(value, salt)
            result[key_hashcode] = value_hashcode

    return result
