from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import \
    GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeGlobalForwardingRuleBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeGlobalForwardingRule:
        return GcpComputeGlobalForwardingRule(name=attributes['name'],
                                              target=attributes['target'])

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_GLOBAL_FORWARDING_RULE
