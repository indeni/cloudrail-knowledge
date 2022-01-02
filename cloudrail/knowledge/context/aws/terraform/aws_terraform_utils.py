import functools
import logging
import re
from dataclasses import dataclass
from typing import List


@dataclass
class ResourcesData:
    resources: List[dict]
    modules: List[str]


class AwsTerraformUtils:
    def __init__(self, plan_json: dict):
        # The primal default region. Will be replaced by the region specified in "aws" provider, or will be the region of "aws" provider if a
        # region was not set.
        self.default_region: str = 'us-east-1'
        self.configuration: dict = plan_json['configuration']
        self.variables: dict = plan_json.get('variables', {})
        self.provider_region_map: dict = self._get_provider_region_map()

    def get_resource_region(self, address: str) -> str:
        try:
            return self._get_resource_region(address)
        except Exception as ex:
            logging.exception(f'An error occurred while trying to get the region of {address}. '
                              f'Will set the default region "{self.default_region}" Instead.\n{str(ex)}')
            return self.default_region

    def _get_provider_region_map(self) -> dict:
        provider_region_map = {}
        if 'provider_config' not in self.configuration:
            self.configuration['provider_config'] = {}

        if 'aws' not in self.configuration['provider_config']:
            self.configuration['provider_config']['aws'] = {'name': 'aws'}

        # Ordering the keys so the default provider "aws" will be handled first, so after we determine its region,
        # we will use its region as the default region when we cannot figure out the real region
        provider_config_keys = list(self.configuration['provider_config'].keys())
        provider_config_keys.insert(0, provider_config_keys.pop(provider_config_keys.index('aws')))

        for provider_config_key in provider_config_keys:
            region = self.get_provider_region(provider_config_key)

            if provider_config_key == 'aws':
                self.default_region = region
            provider_region_map[provider_config_key] = region

        return provider_region_map

    def get_provider_region(self, provider: str):
        if provider not in self.configuration['provider_config']:
            return None
        value = self.configuration['provider_config'][provider]
        region = value.get('expressions', {}).get('region', {}).get('constant_value')
        if not region:
            # When region is defined by a variable
            region_ref = value.get('expressions', {}).get('region', {}).get('references')
            if region_ref:
                region_ref = region_ref[0].replace('var.', '')
                if module_address := value.get('module_address'):
                    # If its a part of a module, then the variable will be in the 'expressions' field of the module section
                    try:
                        module_section = self._get_module_section(module_address, self.configuration['root_module'])
                        region = module_section.get('expressions', {}).get(region_ref, {}).get('constant_value')
                    except Exception as ex:
                        logging.exception(f'An error occurred while trying to get the region of provider {provider}. '
                                          f'Will set "{self.default_region}" Instead.\n{str(ex)}')
                        region = self.default_region
                else:
                    # If its not a part of a module, then the variable should be on the top-level 'variables' field
                    region = self.variables.get(region_ref, {}).get('value')

        if not region:
            logging.warning(f'Couldnt conclude the region for provider {provider}. will assign "{self.default_region}" instead.')
            region = self.default_region

        return region

    @staticmethod
    def _remove_square_brackets_with_content(text: str) -> str:
        pattern = r'\[.*?\]'
        return re.sub(pattern, '', text)

    @classmethod
    def _get_module_section(cls, module_path: str, root_module: dict):
        module_section = root_module
        if module_path.startswith('module.'):
            module_section = root_module['module_calls']
            module_names = cls._get_module_names(module_path)
            for module in module_names[:-1]:
                module_section = module_section[module]['module']['module_calls']
            module_section = module_section[module_names[-1]]

        return module_section

    @staticmethod
    @functools.lru_cache
    def _get_module_names(module_path: str) -> List[str]:
        return list(filter(lambda x: x != 'module', module_path.split('.')))

    def _get_resources_data(self, address: str) -> ResourcesData:
        # Module address is the address minus the resource type and name
        # For example: module.module1.module.module2.aws_vpc.my_vpc
        # In this example, module.module1.module.module2 is the module address
        module_path = '.'.join(address.split('.')[:-2])

        if module_path:
            module_names = self._get_module_names(module_path)
            module_section = self._get_module_section(module_path, self.configuration['root_module'])
            return ResourcesData(module_section['module']['resources'], module_names)
        else:
            return ResourcesData(self.configuration['root_module']['resources'], [])

    def _get_resource_region(self, address: str) -> str:
        original_address = address
        address = self._remove_square_brackets_with_content(address)
        resources_data = self._get_resources_data(address)

        address = '.'.join(address.split('.')[-2:])
        provider_config_key = next(resource.get('provider_config_key') for resource in resources_data.resources if resource['address'] == address)

        if not provider_config_key:
            logging.warning(
                f'Couldnt conclude the provider for resource {original_address}. will use the default region {self.default_region} instead.')
            return self.default_region

        provider_config_key_prefix = ''

        if resources_data.modules:
            # Building the provider_config_key_prefix If the resource is part of a module, then the provider_config_key will be comprised of the
            # module the resource belongs to, and the provider name Which looks like this: "my_module:my_provider_name". However,
            # in the "provider_config" section, the provider keys are built with the entire path of the modules. This is why we are building the
            # provider_config_key_prefix which will be prepended to the original provider_config_key
            for module_name in resources_data.modules:
                provider_config_key_prefix = f'{provider_config_key_prefix}module.{module_name}.'
            provider_config_key_prefix = provider_config_key_prefix[:len(provider_config_key_prefix) - 1] + ':'

        provider_config_key = f'{provider_config_key_prefix}{provider_config_key.split(":")[-1]}'

        while not (region := self.provider_region_map.get(provider_config_key)):
            # This section attempts to find the region for a resource in a module. if the provider is not found with the full module path,
            # then we will search for the relevant provider in the module that called the current module. For example, module A uses module B.
            # Module A defined the default provider, but module B did not. Also, module B defines a resource. The provider data will not be present
            # at the module B level, but rather in module A level.
            module_addresses, provider_name = provider_config_key.split(':')
            module_addresses = module_addresses.split('.')[:-2]
            if module_addresses:
                provider_config_key = f'{".".join(module_addresses)}:{provider_name}'
            else:
                provider_config_key = provider_name

        if not region:
            logging.warning(f'Couldn\'t get region for: "{original_address}". will use the default region {self.default_region} instead.')
            return self.default_region
        return region

    @classmethod
    def clear_cache(cls):
        cls.clear_cache()
