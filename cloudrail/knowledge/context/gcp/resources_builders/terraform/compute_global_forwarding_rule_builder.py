from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import \
    GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeGlobalForwardingRuleBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeGlobalForwardingRule:
        prefix = ''
        if attributes.get('self_link') and 'https:' in attributes.get('self_link', ''):
            prefix = attributes.get('self_link').split('projects')[0]
        return GcpComputeGlobalForwardingRule(name=attributes['name'],
                                              target_identifier=prefix+attributes['target'])

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_GLOBAL_FORWARDING_RULE
