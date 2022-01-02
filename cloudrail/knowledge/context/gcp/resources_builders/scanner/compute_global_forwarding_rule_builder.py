from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_global_forwarding_rule import \
    GcpComputeGlobalForwardingRule
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeGlobalForwardingRuleBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-globalForwardingRules-list.json'

    def do_build(self, attributes: dict) -> GcpComputeGlobalForwardingRule:
        return GcpComputeGlobalForwardingRule(name=attributes['name'],
                                              target_identifier=attributes['target'])
