from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_https_proxy import GcpComputeTargetHttpsProxy
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeTargetHttpsProxyBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-targetHttpsProxies-list.json'

    def do_build(self, attributes: dict) -> GcpComputeTargetHttpsProxy:
        return GcpComputeTargetHttpsProxy(name=attributes['name'],
                                          target_id=attributes['id'],
                                          self_link=attributes['selfLink'],
                                          url_map=attributes['urlMap'],
                                          ssl_certificates=attributes['sslCertificates'],
                                          ssl_policy_identifier=attributes.get('sslPolicy'))
