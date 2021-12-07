from typing import List
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_pool import GcpComputeTargetPool
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeTargetPoolBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeTargetPool:
        return GcpComputeTargetPool(name=attributes['name'],
                                    region=self._get_known_value(attributes, 'region'),
                                    instances=self._convert_zone_name_to_urls(attributes,
                                                                              self._get_known_value(attributes, 'instances')),
                                    self_link=attributes['self_link'])

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_TARGET_POOL

    @staticmethod
    def _convert_zone_name_to_urls(attributes: dict, instances: list) -> List:
        project_id = attributes['_project_id']
        for index, instance in enumerate(instances):
            if 'self_link' not in instance and 'https' not in instance:
                zone, name = instance.split('/')
                instances[index] = f'https://www.googleapis.com/compute/v1/projects/{project_id}/zones/{zone}/instances/{name}'
        return instances
