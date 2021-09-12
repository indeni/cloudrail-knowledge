import functools
import os
from enum import Enum
from typing import Dict, Optional, List
import yaml
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


class FieldAction(str, Enum):
    SKIP = 'skip'
    PASS = 'pass'
    HASH = 'hash'


@dataclass
class KnownFields(DataClassJsonMixin):
    pass_values: Dict[str, Optional['SupportedSection']]
    hash_values: List[str]


@dataclass
class SupportedSection(DataClassJsonMixin):
    known_fields: Optional[KnownFields]
    unknown_fields_action: FieldAction


class IacFieldsStore:

    CURRENT_PATH: str = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def get_azure_supported_services() -> Dict[str, SupportedSection]:
        terraform_fields_file_path = os.path.join(IacFieldsStore.CURRENT_PATH, '../context/azure/terraform/azure_terraform_fields.yaml')
        return IacFieldsStore._get_cloud_provider_supported_services(terraform_fields_file_path)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def get_terraform_aws_supported_services() -> Dict[str, SupportedSection]:
        terraform_fields_file_path = os.path.join(IacFieldsStore.CURRENT_PATH, '../context/aws/terraform/aws_terraform_fields.yaml')
        return IacFieldsStore._get_cloud_provider_supported_services(terraform_fields_file_path)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def get_terraform_gcp_supported_services() -> Dict[str, SupportedSection]:
        terraform_fields_file_path = os.path.join(IacFieldsStore.CURRENT_PATH, '../context/gcp/terraform/gcp_terraform_fields.yaml')
        return IacFieldsStore._get_cloud_provider_supported_services(terraform_fields_file_path)

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def get_cloudformation_supported_services() -> Dict[str, SupportedSection]:
        cfn_fields_file_path = os.path.join(IacFieldsStore.CURRENT_PATH, '../context/aws/cloudformation/cloudformation_fields.yaml')
        return IacFieldsStore._get_cloud_provider_supported_services(cfn_fields_file_path)

    @staticmethod
    def _get_cloud_provider_supported_services(cloud_provider_fields_file_path: str) -> Dict[str, SupportedSection]:
        supported_sections = {}
        with open(cloud_provider_fields_file_path) as file:
            supported_services = yaml.safe_load(file)
            for service in supported_services:
                supported_sections[service] = IacFieldsStore._create_supported_section(supported_services[service])
        return supported_sections

    @classmethod
    def _create_supported_section(cls, raw_section: dict) -> SupportedSection:
        cls._validate_known_fields(raw_section, {'known_fields', 'unknown_fields_action'})
        raw_known_fields = raw_section.get('known_fields')
        if raw_known_fields:
            cls._validate_known_fields(raw_known_fields, {'hash', 'pass'})
            hash_values = [hash_value.lower() for hash_value in raw_known_fields.get('hash', [])]
            raw_pass_values = raw_known_fields.get('pass', [])
            pass_values = {}
            for raw_field in raw_pass_values:
                if isinstance(raw_field, str):
                    pass_values[raw_field.lower()] = None
                else:
                    field_key = list(raw_field.keys())[0]
                    field_value = raw_field[field_key]
                    pass_values[field_key.lower()] = cls._create_supported_section(field_value)
            known_fields = KnownFields(pass_values, hash_values)
            default_unknown_fields_action = FieldAction.SKIP
        else:
            known_fields = None
            default_unknown_fields_action = FieldAction.PASS
        unknown_fields_action = FieldAction(raw_section.get('unknown_fields_action', default_unknown_fields_action))
        return SupportedSection(known_fields, unknown_fields_action)

    @staticmethod
    def _validate_known_fields(dic: dict, known_fields: set):
        unknown_fields = set(dic.keys()) - known_fields
        if unknown_fields:
            raise Exception(f'Unknown fields in terraform_aws_fields {unknown_fields}')
