import copy
import json
import os
from typing import Dict, List

from cloudrail.knowledge.utils.hash_utils import to_hashcode
from cloudrail.knowledge.utils.iac_fields_store import FieldAction, KnownFields, SupportedSection
from cloudrail.knowledge.utils import file_utils


class TerraformShowOutputTransformer:

    @classmethod
    def transform(cls, show_output_path: str, base_dir: str, services_to_include: dict, salt: str):
        dic = file_utils.file_to_json(show_output_path)
        return {'terraform_version': dic['terraform_version'],
                'format_version': dic['format_version'],
                'configuration': {'provider_config': dic['configuration'].get('provider_config', {}),
                                  'root_module': cls._filter_root_module(dic['configuration'].get('root_module'), base_dir)},
                'resource_changes': [
                    cls._filter_resource(resource, services_to_include, salt)
                    for resource in dic['resource_changes'] if resource['type'] in services_to_include.keys()],
                'variables': dic.get('variables', {})}

    @classmethod
    def transform_original_show(cls, dic: dict,  services_to_include: dict, salt: str):
        return {'terraform_version': dic['terraform_version'],
                'format_version': dic['format_version'],
                'configuration': {'provider_config': dic['configuration'].get('provider_config', {}),
                                  'root_module': dic['configuration'].get('root_module')},
                'resource_changes': [
                    cls._filter_resource(resource, services_to_include, salt)
                    for resource in dic['resource_changes'] if resource['type'] in services_to_include.keys()],
                'variables': dic.get('variables', {})}

    @classmethod
    def _filter_resource(cls, resource: dict,
                         services_to_include: Dict[str, SupportedSection],
                         salt: str):
        resource_type = resource['type']
        supported_section = cls._get_normalized_supported_section(resource_type, services_to_include)
        return {'address': resource.get('address'), 'type': resource.get('type'),
                'name': resource.get('name'), 'mode': resource.get('mode'), 'provider_name': resource.get('provider_name'),
                'change': cls._filter_change_dict(resource.get('change'), supported_section, salt)}

    @staticmethod
    def _get_normalized_supported_section(resource_type: str,
                                          services_to_include: Dict[str, SupportedSection]) -> SupportedSection:
        common_section: SupportedSection = services_to_include['common']
        resource_supported_section = services_to_include.get(resource_type)
        if not resource_supported_section:
            return common_section
        resource_supported_section = copy.deepcopy(resource_supported_section)
        resource_known_fields = services_to_include[resource_type].known_fields or KnownFields({}, [])
        known_fields = copy.deepcopy(common_section.known_fields)
        known_fields.pass_values.update(resource_known_fields.pass_values)
        known_fields.hash_values.extend(resource_known_fields.hash_values)
        resource_supported_section.known_fields = known_fields
        return resource_supported_section

    @classmethod
    def _filter_change_dict(cls, change: dict, supported_section: SupportedSection, salt: str):
        return {'before': cls._filter_fields(change.get('before'), supported_section, salt),
                'after': cls._filter_fields(change.get('after'), supported_section, salt),
                'after_unknown': cls._filter_fields(change.get('after_unknown'), supported_section, salt),
                'actions': change.get('actions')}

    @classmethod
    def _normalize_tags_field(cls, dic: dict):
        for tag_key in ('tags_all', 'tags', 'tag'):
            if dic and dic.get(tag_key) and isinstance(dic[tag_key], list) and isinstance(dic[tag_key][0], dict) and 'key' in dic[tag_key][0].keys():
                dic[tag_key] = {tags_dict['key']: tags_dict['value'] for tags_dict in dic[tag_key]}

    @classmethod
    def _filter_fields(cls, dic: dict, supported_section: SupportedSection, salt: str):
        cls._normalize_tags_field(dic)
        if not dic:
            return dic
        result = {}
        for key in dic.keys():
            value = dic[key]
            if supported_section.known_fields:
                if key.lower() in supported_section.known_fields.pass_values:
                    result[key] = cls._get_passed_field(key.lower(), value, supported_section, salt)
                    continue
                if key.lower() in supported_section.known_fields.hash_values:
                    cls._add_to_dic_as_hash(key, value, result, salt)
                    continue
            if supported_section.unknown_fields_action == FieldAction.PASS:
                result[key] = value
                continue
            if supported_section.unknown_fields_action == FieldAction.HASH:
                cls._add_to_dic_as_hash(key, value, result, salt)
                continue
        return result

    @classmethod
    def _get_passed_field(cls, key, value, supported_section, salt):
        known_key_value = supported_section.known_fields.pass_values.get(key)
        if known_key_value:
            if value is not None and not isinstance(value, list) and not isinstance(value, dict):
                try:
                    json_value = json.loads(value)
                    if isinstance(json_value, list):
                        return json.dumps([cls._filter_fields(field, known_key_value, salt) for field in json_value])
                    if isinstance(json_value, dict):
                        return json.dumps(cls._filter_fields(json_value, known_key_value, salt))
                except Exception:
                    return value
            if isinstance(value, list):
                return [cls._filter_fields(field, known_key_value, salt) for field in value]
            if isinstance(value, dict):
                return cls._filter_fields(value, known_key_value, salt)
        return value

    @classmethod
    def _add_to_dic_as_hash(cls, key: str, value: str, dic: dict, salt):
        hash_key = f'{key}_hashcode'
        dic[hash_key] = value and to_hashcode(value, salt)

    @classmethod
    def _filter_root_module(cls, root_module: dict, base_dir: str):
        result = {'resources': cls._filter_resources(root_module.get('resources', []), base_dir)}
        module_calls = root_module.get('module_calls', {})
        result['module_calls'] = {module: cls._filter_module(module_calls.get(module), base_dir) for module in module_calls.keys()}
        return result

    @classmethod
    def _filter_resources(cls, resources: List[dict], base_dir: str):
        return [{'address': resource.get('address'),
                 'provider_config_key': resource.get('provider_config_key'),
                 'raw_data': cls._prepend_base_dir_to_raw_data(resource.get('raw_data', {}), base_dir)} for resource in resources]

    @classmethod
    def _filter_module(cls, module: dict, base_dir: str):
        filtered_module = {'resources': cls._filter_resources(module['module'].get('resources', []), base_dir)}
        if module.get('module').get('module_calls'):
            filtered_module['module_calls'] = {key: cls._filter_module(value, base_dir) for (key, value) in
                                               module.get('module').get('module_calls').items()}
        raw_data = cls._prepend_base_dir_to_raw_data(module.get('raw_data'), base_dir)
        return {'raw_data': raw_data, 'module': filtered_module, 'expressions': module.get('expressions', {})}

    @staticmethod
    def _prepend_base_dir_to_raw_data(raw_data, base_dir):
        if not base_dir or not raw_data:
            return raw_data
        raw_data['FileName'] = os.path.join(base_dir, raw_data['FileName'])
        return raw_data
