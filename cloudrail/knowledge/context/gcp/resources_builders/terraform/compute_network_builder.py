from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork, \
    GcpComputeNetworkRoutingMode
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeNetworkBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeNetwork:
        return GcpComputeNetwork(name=attributes['name'],
                                 network_id=attributes["id"],
                                 self_link=attributes["self_link"],
                                 auto_create_subnetworks=self._get_known_value(attributes, 'auto_create_subnetworks', True),
                                 routing_mode=GcpComputeNetworkRoutingMode(self._get_known_value(attributes, 'routing_mode', 'REGIONAL')))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_NETWORK
