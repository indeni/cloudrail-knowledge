import re
from cloudrail.knowledge.utils.port_set import PortSet
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import \
    BaseGcpTerraformBuilder


class ComputeForwardingRuleBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeForwardingRule:
        port_range = None
        if port_range := self._get_known_value(attributes, 'port_range'):
            port_range = PortSet([port_range])
        return GcpComputeForwardingRule(name=attributes['name'],
                                        target=self._formalize_target_link(self._get_known_value(attributes, 'target')),
                                        port_range=port_range)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_FORWARDING_RULE

    @staticmethod
    def _formalize_target_link(link: str) -> str:
        if 'https://www.googleapis.com/compute/' in link and '/v1/' not in link:
            splitted_link = link.split('https://www.googleapis.com/compute/')
            prefix_link = re.sub(r"^\w+\/", 'v1', splitted_link[1])
            return splitted_link[0] + prefix_link
        return link
