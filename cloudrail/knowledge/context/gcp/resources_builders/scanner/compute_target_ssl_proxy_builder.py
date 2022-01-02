from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_ssl_proxy import GcpComputeTargetSslProxy
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeTargetSslProxyBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-targetSslProxies-list.json'

    def do_build(self, attributes: dict) -> GcpComputeTargetSslProxy:
        name = attributes["name"]
        target_id = attributes["id"]
        self_link = attributes["selfLink"]
        backend_service = attributes["service"]
        ssl_certificates = attributes["sslCertificates"]
        ssl_policy_identifier = attributes.get("sslPolicy")
        return GcpComputeTargetSslProxy(name, target_id, self_link, backend_service, ssl_certificates, ssl_policy_identifier)
