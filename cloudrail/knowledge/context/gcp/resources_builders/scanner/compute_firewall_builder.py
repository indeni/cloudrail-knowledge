from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_firewall import GcpComputeFirewall, GcpComputeFirewallAction, FirewallRuleAction, GcpComputeFirewallDirection
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_set import PortSet


class ComputeFirewallBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-firewalls-list.json'

    def do_build(self, attributes: dict) -> GcpComputeFirewall:
        # Allow Firewall Actions:
        allow_actions = []
        if firewall_actions := attributes.get('allowed'):
            for action in firewall_actions:
                firewall_action_data = self.get_action_block_data(action)
                allow_actions.append(GcpComputeFirewallAction(firewall_action_data['protocol'],
                                                              firewall_action_data['ports'],
                                                              FirewallRuleAction.ALLOW))

        # Deny Firewall Actions:
        deny_actions = []
        if firewall_actions := attributes.get('denied'):
            for action in firewall_actions:
                firewall_action_data = self.get_action_block_data(action)
                deny_actions.append(GcpComputeFirewallAction(firewall_action_data['protocol'],
                                                             firewall_action_data['ports'],
                                                             FirewallRuleAction.DENY))
        direction = GcpComputeFirewallDirection.INGRESS
        if direction_data := attributes.get('direction'):
            direction = GcpComputeFirewallDirection(direction_data)
        return GcpComputeFirewall(name=attributes['name'],
                                  network=attributes['network'],
                                  allow=allow_actions,
                                  deny=deny_actions,
                                  destination_ranges=attributes.get('destinationRanges'),
                                  direction=direction,
                                  source_ranges=attributes.get('sourceRanges'),
                                  priority=attributes['priority'],
                                  source_tags=attributes.get('sourceTags'),
                                  disabled=attributes.get('disabled', True))

    @staticmethod
    def get_action_block_data(attributes: dict) -> dict:
        protocol = IpProtocol(attributes['IPProtocol'])
        ports = PortSet(attributes.get('ports', ['0-65535']))
        return {'protocol': protocol, 'ports': ports}
