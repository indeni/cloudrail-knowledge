from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_node_pool import GcpContainerNodePool, GcpClusterNodePoolAutoscaling, GcpClusterNodePoolManagement
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.context.gcp.resources_builders.scanner.container_cluster_builder import ContainerClusterBuilder


class ContainerNodePoolBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'container-node-pools.json'

    def do_build(self, attributes: dict) -> GcpContainerNodePool:
        # Autoscaling
        autoscaling = None
        if autoscaling_data := attributes.get('autoscaling'):
            autoscaling = GcpClusterNodePoolAutoscaling(min_node_count=autoscaling_data['minNodeCount'],
                                                        max_node_count=autoscaling_data['maxNodeCount'])
        # Management
        management_data = attributes['management']
        management = GcpClusterNodePoolManagement(auto_repair=management_data['autoRepair'],
                                                  auto_upgrade=management_data['autoUpgrade'])

        return GcpContainerNodePool(name=attributes["name"],
                                    cluster=attributes['selfLink'].split('/')[9],
                                    location=attributes['selfLink'].split('/')[7],
                                    autoscaling=autoscaling,
                                    management=management,
                                    node_config=ContainerClusterBuilder.build_container_cluster_node_config(attributes['config']))
