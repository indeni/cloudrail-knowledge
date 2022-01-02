

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_pool import GcpComputeTargetPool
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class ComputeTargetPoolBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'compute-v1-targetPools-list.json'

    def do_build(self, attributes: dict) -> GcpComputeTargetPool:
        return GcpComputeTargetPool(name=attributes['name'],
                                    region=attributes['region'],
                                    instances=attributes['instances'],
                                    self_link=attributes['selfLink'])
