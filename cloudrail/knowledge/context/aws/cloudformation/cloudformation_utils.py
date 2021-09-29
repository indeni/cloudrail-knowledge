import re
from typing import Optional

import yaml
from cfn_tools import load_json, load_yaml, ODict, CfnYamlLoader
from cfn_tools.yaml_dumper import TAG_MAP
from cloudrail.knowledge.context.cloud_provider import CloudProvider
from cloudrail.knowledge.context.iac_type import IacType
from cloudrail.knowledge.utils.file_utils import read_file
from cloudrail.knowledge.utils.string_utils import StringUtils

ELEMENT_POSITION_KEY: str = 'cfn_resource_block_position'
NODE_KEY_LINE_REGEX: str = '"{}"\\s*:'


# pylint: disable=R1710
class CustomCloudformationLoader(CfnYamlLoader):
    pass


def construct_mapping(self, node, deep=False):
    """
    Use ODict for maps
    """

    mapping = ODict()
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        value = self.construct_object(value_node, deep=deep)
        mapping[key] = value

    if 'Type' in mapping and ELEMENT_POSITION_KEY not in mapping:
        mapping[ELEMENT_POSITION_KEY] = (node.start_mark.line, node.end_mark.line - 1)

    return mapping


CustomCloudformationLoader.add_constructor(TAG_MAP, construct_mapping)


class CloudformationUtils:

    EXTRA_PARAMETERS_KEY: str = 'cr_extra_params'

    @classmethod
    def validate_required_cfn_template_parameters(cls, cfn_template_file: str, cfn_template_parameters: dict):
        cfn_template_content: dict = cls.load_cfn_template(cfn_template_file)
        template_parameters: dict = cfn_template_content.get('Parameters', {})
        for param_name in template_parameters:
            if param_name not in cfn_template_parameters and 'Default' not in template_parameters[param_name]:
                raise Exception(f'Missing required template parameter "{param_name}"')

    @classmethod
    def create_cfn_template_extra_parameters(cls, cfn_stack_name: str, iac_type: IacType, cloud_provider: CloudProvider,
                                             cfn_stack_region: str, account_id: str, cfn_template_file_name: str,
                                             account_name: Optional[str] = None, cfn_parameters: dict = None) -> dict:
        extra_parameters = {'stack_name': cfn_stack_name,
                            'iac_type': iac_type,
                            'cloud_provider': cloud_provider,
                            'region': cfn_stack_region,
                            'account_id': account_id,
                            'cfn_template_file_name': cfn_template_file_name}

        if account_name:
            extra_parameters['account_name'] = account_name

        if cfn_parameters:
            extra_parameters.update(cfn_parameters)
        return extra_parameters

    @classmethod
    def load_cfn_template(cls, cfn_template_file: str) -> dict:
        if cfn_template_file.endswith('.json'):
            return cls.file_to_cfn_json(cfn_template_file)
        elif cfn_template_file.endswith('.yaml'):
            return cls.file_to_cfn_yaml(cfn_template_file)
        else:
            cls.raise_invalid_cfn_template_file()

    @classmethod
    def cfn_template_str_to_dict(cls, cfn_template_content: str) -> dict:
        if StringUtils.is_json(cfn_template_content):
            return load_json(cfn_template_content)
        elif StringUtils.is_yaml(cfn_template_content):
            return load_yaml(cfn_template_content)
        else:
            cls.raise_invalid_cfn_template_file()

    @classmethod
    def file_to_cfn_json(cls, file_path: str) -> dict:
        try:
            cfn_template_content: str = read_file(file_path)
            cfn_template_as_dict: dict = load_json(cfn_template_content)
            cls._set_cfn_resources_block_position(cfn_template_as_dict, file_path)
            return cfn_template_as_dict
        except Exception as ex:
            message = f'Error while reading CloudFormation template JSON file {file_path}. {ex}'
            raise Exception(message)

    @staticmethod
    def file_to_cfn_yaml(file_path: str) -> dict:
        try:
            return yaml.load(stream=read_file(file_path), Loader=CustomCloudformationLoader)
        except Exception as ex:
            message = f'error while reading CloudFormation template yaml file {file_path}. {ex}'
            raise Exception(message)

    @staticmethod
    def to_odict(ordinary_dict: dict) -> ODict:
        return ODict([[key, val] for key, val in ordinary_dict.items()])

    @staticmethod
    def raise_invalid_cfn_template_file():
        raise Exception('Invalid CloudFormation template file format')

    @classmethod
    def _set_cfn_resources_block_position(cls, cfn_template_as_dict: dict, file_path: str):
        json_doc: str = read_file(file_path)
        cfn_resources: dict = cfn_template_as_dict.get('Resources', {})
        for resource_name, cfn_resource in cfn_resources.items():
            if ELEMENT_POSITION_KEY not in cfn_resource:
                key_pattern: str = NODE_KEY_LINE_REGEX.format(resource_name)
                pattern_occurrences: list = re.split(key_pattern, json_doc)
                if len(pattern_occurrences) > 1:
                    start_line: int = pattern_occurrences[0].count('\n') + 1
                    end_line: int = start_line + cls._end_element_line_number(pattern_occurrences[-1])
                    cfn_resource[ELEMENT_POSITION_KEY] = (start_line, end_line)

    @staticmethod
    def _end_element_line_number(pattern_occurrence: str):
        open_braces_counter: int = 0
        already_opened: bool = False
        index: int = 0
        for character in pattern_occurrence:
            if character == '{':
                already_opened = True
                open_braces_counter += 1
            elif character == '}':
                open_braces_counter -= 1

            if already_opened and open_braces_counter == 0:
                break
            index += 1
        sub_str: str = pattern_occurrence[0: index]
        return sub_str.count('\n')
