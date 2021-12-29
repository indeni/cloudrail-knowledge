from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_http_proxy import GcpComputeTargetHttpProxy
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeTargetHttpProxyBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-targetHttpProxies-list.json'

    def do_build(self, attributes: dict) -> GcpComputeTargetHttpProxy:
        return GcpComputeTargetHttpProxy(name=attributes['name'],
                                         target_id=attributes["id"],
                                         self_link=attributes["selfLink"],
                                         url_map=attributes['urlMap'])
