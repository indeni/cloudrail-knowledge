from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_network import GcpComputeNetwork, \
    GcpComputeNetworkRoutingMode
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeNetworkBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-networks-list.json'

    def do_build(self, attributes: dict) -> GcpComputeNetwork:
        routing_mode = attributes['routingConfig'].get('routingMode', 'REGIONAL') if attributes.get('routingConfig') else 'REGIONAL'
        return GcpComputeNetwork(name=attributes['name'],
                                 network_id=attributes["id"],
                                 self_link=attributes["selfLink"],
                                 auto_create_subnetworks=attributes.get('autoCreateSubnetworks', True),
                                 routing_mode=GcpComputeNetworkRoutingMode(routing_mode))
