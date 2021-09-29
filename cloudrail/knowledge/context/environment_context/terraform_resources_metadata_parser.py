from typing import Optional, Dict
from cloudrail.knowledge.context.iac_resource_metadata import IacResourceMetadata


class TerraformResourcesMetadataParser:

    @staticmethod
    def parse(configuration: dict) -> Dict[str, IacResourceMetadata]:
        result = {}
        root_module_content = configuration.get('root_module', {})
        TerraformResourcesMetadataParser._fill_module_content(root_module_content, None, result)
        return result

    @staticmethod
    def _fill_module_content(content: dict,
                             module_metadata: Optional[IacResourceMetadata],
                             result: Dict[str, IacResourceMetadata]):
        TerraformResourcesMetadataParser._add_resources(content, module_metadata, result)
        TerraformResourcesMetadataParser._add_modules(content, module_metadata, result)

    @staticmethod
    def _add_resources(content: dict,
                       module_metadata: Optional[IacResourceMetadata],
                       result: Dict[str, IacResourceMetadata]):
        resources = content.get('resources', [])
        for resource in resources:
            metadata = TerraformResourcesMetadataParser._create_resource_metadata(resource,
                                                                                  resource['address'],
                                                                                  module_metadata)
            result[metadata.iac_entity_id] = metadata

    @staticmethod
    def _add_modules(content: dict,
                     module_metadata: Optional[IacResourceMetadata],
                     result: Dict[str, IacResourceMetadata]):
        module_calls = content.get('module_calls', {})
        for module_name in module_calls:
            data = module_calls[module_name]
            address = 'module.{}'.format(module_name)
            resource_metadata = TerraformResourcesMetadataParser._create_resource_metadata(data,
                                                                                           address,
                                                                                           module_metadata)
            TerraformResourcesMetadataParser._fill_module_content(data['module'],
                                                                  resource_metadata, result)

    @staticmethod
    def _create_resource_metadata(data: dict,
                                  address: str,
                                  module_metadata: Optional[IacResourceMetadata]):
        ancestor_address = '{}.'.format(module_metadata.iac_entity_id) if module_metadata else ''
        raw_data = data.get('raw_data', {})
        address = '{}{}'.format(ancestor_address, address)
        metadata = IacResourceMetadata(iac_entity_id=address,
                                       file_name=raw_data.get('FileName'),
                                       start_line=raw_data.get('StartLine'),
                                       end_line=raw_data.get('EndLine'),
                                       module_metadata=module_metadata)
        return metadata
