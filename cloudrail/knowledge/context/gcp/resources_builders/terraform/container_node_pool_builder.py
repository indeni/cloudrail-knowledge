from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_node_pool import GcpContainerNodePool, GcpClusterNodePoolAutoscaling, GcpClusterNodePoolManagement
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.container_cluster_builder import ContainerClusterBuilder


class ContainerNodePoolBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpContainerNodePool:
        # node pool name
        name = attributes['name']
        if '/' in name:
            name = name.split('clusters/')[-1]

        # Autoscaling
        autoscaling = None
        if autoscaling_data := self._get_known_value(attributes, 'autoscaling'):
            autoscaling = GcpClusterNodePoolAutoscaling(min_node_count=autoscaling_data[0]['min_node_count'],
                                                        max_node_count=autoscaling_data[0]['max_node_count'])
        # Management
        management = GcpClusterNodePoolManagement(True, True)
        if management_data := self._get_known_value(attributes, 'management'):
            management = GcpClusterNodePoolManagement(auto_repair=self._get_known_value(management_data[0], 'auto_repair', True),
                                                      auto_upgrade=self._get_known_value(management_data[0], 'auto_upgrade', True))

        return GcpContainerNodePool(name=name,
                                    cluster=attributes['cluster'],
                                    location=self._get_known_value(attributes, 'location'),
                                    autoscaling=autoscaling,
                                    management=management,
                                    node_config=ContainerClusterBuilder.build_container_cluster_node_config(attributes))

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_CONTAINER_NODE_POOL
