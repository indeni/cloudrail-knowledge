from cloudrail.knowledge.context.environment_context.common_component_builder import extract_name_from_gcp_link
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork, GcpComputeSubNetworkLogConfig
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeSubNetworkBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-subnetworks-list.json'

    def do_build(self, attributes: dict) -> GcpComputeSubNetwork:
        name = attributes["name"]
        subnetwork_id = attributes["id"]
        self_link = attributes["selfLink"]
        region_link = attributes.get("region")
        region = extract_name_from_gcp_link(region_link)
        network_identifier = attributes["network"]
        ip_cidr_range = attributes["ipCidrRange"]
        log_config = self.build_log_config_block(attributes)

        return GcpComputeSubNetwork(name, subnetwork_id, self_link, region, network_identifier, ip_cidr_range, log_config)

    @staticmethod
    def build_log_config_block(attribute: dict) -> GcpComputeSubNetworkLogConfig:
        if log_config_block := attribute.get("logConfig"):
            enabled = log_config_block.get("enable", False)
            aggregation_interval = log_config_block.get("aggregationInterval")
            flow_sampling = log_config_block.get("flowSampling")
            metadata = log_config_block.get("metadata")
            metadata_fields = log_config_block.get("metadataFields")
            filter_expr = log_config_block.get("filterExpr")

            return GcpComputeSubNetworkLogConfig(enabled, aggregation_interval, flow_sampling, metadata, metadata_fields, filter_expr)

        return GcpComputeSubNetworkLogConfig(False, None, None, None, None, None)
