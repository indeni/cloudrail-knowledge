from typing import List

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork, \
    GcpComputeNetworkRoutingMode
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeNetworkBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeNetwork:
        return GcpComputeNetwork(name=attributes['name'],
                                 auto_create_subnetworks=self._get_known_value(attributes, 'auto_create_subnetworks', True),
                                 routing_mode=GcpComputeNetworkRoutingMode(self._get_known_value(attributes, 'routing_mode', 'REGIONAL')),
                                 delete_default_routes_on_create=self._get_known_value(attributes,
                                                                                       'delete_default_routes_on_create',
                                                                                       False),
                                 project=self._get_known_value(attributes, 'project'))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_NETWORK
