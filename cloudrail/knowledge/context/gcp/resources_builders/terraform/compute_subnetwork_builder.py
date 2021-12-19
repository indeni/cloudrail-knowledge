from cloudrail.knowledge.context.environment_context.common_component_builder import extract_name_from_gcp_link
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_subnetwork import GcpComputeSubNetwork, GcpComputeSubNetworkLogConfig
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeSubNetworkBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeSubNetwork:
        name = attributes["name"]
        subnetwork_id = attributes["id"]
        self_link = attributes["self_link"]
        region_link = self._get_known_value(attributes, "region")
        region = extract_name_from_gcp_link(region_link)
        network_identifier = attributes["network"]
        ip_cidr_range = attributes["ip_cidr_range"]
        log_config = self.build_log_config_block(attributes)

        return GcpComputeSubNetwork(name, subnetwork_id, self_link, region, network_identifier, ip_cidr_range, log_config)

    def build_log_config_block(self, attribute: dict) -> GcpComputeSubNetworkLogConfig:
        if log_config_block := attribute.get("log_config"):
            log_config_block = log_config_block[0]
            aggregation_interval = self._get_known_value(log_config_block, "aggregation_interval")
            flow_sampling = self._get_known_value(log_config_block, "flow_sampling")
            metadata = self._get_known_value(log_config_block, "metadata")
            metadata_fields = self._get_known_value(log_config_block, "metadata_fields")
            filter_expr = self._get_known_value(log_config_block, "filter_expr")

            return GcpComputeSubNetworkLogConfig(True, aggregation_interval, flow_sampling, metadata, metadata_fields, filter_expr)

        return GcpComputeSubNetworkLogConfig(False, None, None, None, None, None)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_SUBNETWORK
