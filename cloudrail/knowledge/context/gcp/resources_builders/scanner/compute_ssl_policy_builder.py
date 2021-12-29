from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_ssl_policy import GcpComputeSslPolicy
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeSslPolicyBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-sslPolicies-list.json'

    def do_build(self, attributes: dict) -> GcpComputeSslPolicy:
        name = attributes["name"]
        policy_id = attributes["id"]
        self_link = attributes["selfLink"]
        min_tls_version = attributes["minTlsVersion"]
        profile = attributes["profile"]
        custom_features = attributes.get("customFeatures")
        return GcpComputeSslPolicy(name, policy_id, self_link, min_tls_version, profile, custom_features)
