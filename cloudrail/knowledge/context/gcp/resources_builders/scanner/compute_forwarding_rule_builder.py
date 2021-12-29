from cloudrail.knowledge.utils.port_set import PortSet
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_forwarding_rule import GcpComputeForwardingRule
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeForwardingRuleBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-forwardingRules-list.json'

    def do_build(self, attributes: dict) -> GcpComputeForwardingRule:
        return GcpComputeForwardingRule(name=attributes['name'],
                                        target=attributes['target'],
                                        port_range=PortSet([attributes['portRange']]))
