from typing import Callable
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall, GcpComputeFirewallAction, FirewallRuleAction, GcpComputeFirewallDirection
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_set import PortSet


class ComputeFirewallBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpComputeFirewall:
        # Allow Firewall Actions:
        allow_actions = []
        if firewall_actions := self._get_known_value(attributes, 'allow'):
            for action in firewall_actions:
                firewall_action_data = self.get_action_block_data(action, self._get_known_value)
                allow_actions.append(GcpComputeFirewallAction(firewall_action_data['protocol'],
                                                              firewall_action_data['ports'],
                                                              FirewallRuleAction.ALLOW))

        # Deny Firewall Actions:
        deny_actions = []
        if firewall_actions := self._get_known_value(attributes, 'deny'):
            for action in firewall_actions:
                firewall_action_data = self.get_action_block_data(action, self._get_known_value)
                deny_actions.append(GcpComputeFirewallAction(firewall_action_data['protocol'],
                                                             firewall_action_data['ports'],
                                                             FirewallRuleAction.DENY))

        direction = GcpComputeFirewallDirection.INGRESS
        if direction_data := self._get_known_value(attributes, 'direction'):
            direction = GcpComputeFirewallDirection(direction_data)
        return GcpComputeFirewall(name=attributes['name'],
                                  network=attributes['network'],
                                  allow=allow_actions,
                                  deny=deny_actions,
                                  destination_ranges=self._get_known_value(attributes, 'destination_ranges'),
                                  direction=direction,
                                  source_ranges=self._get_known_value(attributes, 'source_ranges'),
                                  priority=self._get_known_value(attributes, 'priority', 1000),
                                  source_tags=self._get_known_value(attributes, 'source_tags'),
                                  disabled=self._get_known_value(attributes, 'disabled', False))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_COMPUTE_FIREWALL

    @staticmethod
    def get_action_block_data(attributes: dict, get_known_value_func: Callable) -> dict:
        protocol = IpProtocol(attributes['protocol'])
        ports = PortSet(get_known_value_func(attributes, 'ports', ['0-65535']))
        return {'protocol': protocol, 'ports': ports}
