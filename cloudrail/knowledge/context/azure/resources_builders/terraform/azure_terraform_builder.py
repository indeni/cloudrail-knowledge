from typing import List

from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource

from cloudrail.knowledge.context.base_context_builders.base_terraform_builder import BaseTerraformBuilder


class AzureTerraformBuilder(BaseTerraformBuilder):

    def do_build(self, attributes: dict):
        pass

    def get_service_name(self):
        pass

    def build(self) -> List[AzureResource]:
        all_attributes = self.resources.get(self.get_service_name().value)
        if not all_attributes:
            return []

        result = []
        for attributes in all_attributes:
            build_result = self._build_and_map_action(attributes)
            if build_result:
                if isinstance(build_result, list):
                    for item in build_result:
                        self._set_common_attributes(item, attributes)
                        result.append(item)
                else:
                    self._set_common_attributes(build_result, attributes)
                    result.append(build_result)

        return result

    @staticmethod
    def _set_common_attributes(resource: AzureResource, attributes: dict):
        if not isinstance(resource, AzureResource):
            return
        resource.subscription_id = attributes['subscription_id']
        resource.location = attributes.get('location')
        resource.resource_group_name = attributes.get('resource_group_name')
        resource.tenant_id = attributes['tenant_id']
        if not resource.get_id() and (_id := attributes.get('id')):
            resource.set_id(_id)
            resource.with_aliases(_id)