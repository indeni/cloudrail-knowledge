from typing import List
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources_builders.common_resource_builder_functions import get_normalized_azure_location
from cloudrail.knowledge.context.base_context_builders.base_terraform_builder import BaseTerraformBuilder


class AzureTerraformBuilder(BaseTerraformBuilder):

    def do_build(self, attributes: dict):
        pass

    def get_service_name(self):
        pass

    def _build(self) -> List[AzureResource]:
        all_attributes = self.resources.get(self.get_service_name().value)
        if not all_attributes:
            return []

        result = []
        for attributes in all_attributes:
            build_result = self._build_and_map_action(attributes)
            for resource in build_result if isinstance(build_result, list) else [build_result]:
                if resource:
                    self._set_common_attributes(resource, attributes)
                    result.append(resource)

        return result

    @staticmethod
    def _set_common_attributes(resource: AzureResource, attributes: dict):
        if not isinstance(resource, AzureResource):
            return
        resource.subscription_id = attributes['subscription_id']
        resource.location = get_normalized_azure_location(attributes.get('location'))
        resource.resource_group_name = attributes.get('resource_group_name')
        resource.tenant_id = attributes['tenant_id']
        if resource.is_tagable:
            resource.tags = attributes.get('tags')
        if not resource.get_id() and (_id := attributes.get('id')):
            resource.set_id(_id)
            resource.with_aliases(_id)
