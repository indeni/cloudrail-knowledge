from typing import List
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource
from cloudrail.knowledge.context.base_context_builders.base_terraform_builder import BaseTerraformBuilder


class BaseGcpTerraformBuilder(BaseTerraformBuilder):

    def do_build(self, attributes: dict):
        pass

    def get_service_name(self) -> GcpResourceType:
        pass

    def _build(self) -> List[GcpResource]:
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
    def _set_common_attributes(resource: GcpResource, attributes: dict):
        if not isinstance(resource, GcpResource):
            return

        resource.project_id = attributes['_project_id']
        if not resource.labels:
            resource.labels = attributes.get('labels')
