from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfigCidrBlk,\
    GcpContainerMasterAuthNetConfig, GcpContainerClusterAuthGrpConfig, GcpContainerClusterNetworkPolicy, GcpContainerClusterNetworkConfigProvider
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class ContainerClusterBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpContainerCluster:
        name = attributes["name"]
        location = self._get_known_value(attributes, "location")
        cluster_ipv4_cidr = self._get_known_value(attributes, "cluster_ipv4_cidr")
        enable_shielded_nodes = attributes.get("enable_shielded_nodes")
        master_authorized_networks_config_list = self._get_known_value(attributes, "master_authorized_networks_config")
        master_authorized_networks_config = self.build_master_authorized_networks_config(master_authorized_networks_config_list[0]) if master_authorized_networks_config_list else None
        authenticator_groups_config_block = self._get_known_value(attributes, "authenticator_groups_config")
        authenticator_groups_config = GcpContainerClusterAuthGrpConfig(authenticator_groups_config_block[0]["security_group"]) if authenticator_groups_config_block else None

        ## Network Config
        network_policy = GcpContainerClusterNetworkPolicy(GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED, False)
        if network_policy_data := self._get_known_value(attributes, 'network_policy'):
            network_policy = GcpContainerClusterNetworkPolicy(provider=enum_implementation(GcpContainerClusterNetworkConfigProvider,
                                                                                           self._get_known_value(network_policy_data[0], 'provider'),
                                                                                           GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED),
                                                              enabled=self._get_known_value(network_policy_data[0], 'enabled', False))

        enable_binary_authorization = self._get_known_value(attributes, 'enable_binary_authorization', False)
        container_cluster = GcpContainerCluster(name, location, cluster_ipv4_cidr, enable_shielded_nodes, master_authorized_networks_config,
                                                authenticator_groups_config, network_policy, enable_binary_authorization)
        container_cluster.labels = self._get_known_value(attributes, "resource_labels")

        return container_cluster

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_CONTAINER_CLUSTER

    @staticmethod
    def build_master_authorized_networks_config(master_authorized_networks_config: dict) -> GcpContainerMasterAuthNetConfig:
        cidr_blocks_list = master_authorized_networks_config.get("cidr_blocks", [])
        cidr_blocks = [GcpContainerMasterAuthNetConfigCidrBlk(cidr_block.get("cidr_block"), cidr_block.get("display_name")
                                                              if cidr_block.get("display_name") else None) for cidr_block in cidr_blocks_list]

        return GcpContainerMasterAuthNetConfig(cidr_blocks)
