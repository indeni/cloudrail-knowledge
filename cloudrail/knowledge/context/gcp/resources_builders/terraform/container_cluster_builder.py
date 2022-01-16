from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfigCidrBlk,\
    GcpContainerMasterAuthNetConfig, GcpContainerClusterAuthGrpConfig, GcpContainerClusterNetworkConfig, GcpContainerClusterNetworkConfigProvider, \
    GcpContainerClusterPrivateClusterConfig, GcpContainerClusterShielededInstanceConfig, GcpContainerClusterWorkloadMetadataConfigMode, \
    GcpContainerClusterReleaseChannel
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class ContainerClusterBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpContainerCluster:
        name = attributes["name"]
        location = self._get_known_value(attributes, "location")
        cluster_ipv4_cidr = self._get_known_value(attributes, "cluster_ipv4_cidr")
        enable_shielded_nodes = self._get_known_value(attributes, 'enable_shielded_nodes', True)
        master_authorized_networks_config_list = self._get_known_value(attributes, "master_authorized_networks_config")
        master_authorized_networks_config = self.build_master_authorized_networks_config(master_authorized_networks_config_list[0]) if master_authorized_networks_config_list else None
        authenticator_groups_config_block = self._get_known_value(attributes, "authenticator_groups_config")
        authenticator_groups_config = GcpContainerClusterAuthGrpConfig(authenticator_groups_config_block[0]["security_group"]) if authenticator_groups_config_block else None

        ## Network Config
        network_config = GcpContainerClusterNetworkConfig(GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED, False)
        if network_config_data := self._get_known_value(attributes, 'network_policy'):
            network_config = GcpContainerClusterNetworkConfig(provider=enum_implementation(GcpContainerClusterNetworkConfigProvider,
                                                                                           self._get_known_value(network_config_data[0], 'provider'),
                                                                                           GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED),
                                                              enabled=self._get_known_value(network_config_data[0], 'enabled', False))
        ## Private cluster config
        private_cluster_config = None
        if private_cluster_config_data := self._get_known_value(attributes, 'private_cluster_config'):
            master_global_access_config = False
            if master_global_access_config_data := self._get_known_value(private_cluster_config_data[0], 'master_global_access_config'):
                master_global_access_config = self._get_known_value(master_global_access_config_data[0], 'enabled', False)
            private_cluster_config = GcpContainerClusterPrivateClusterConfig(
                enable_private_nodes=self._get_known_value(private_cluster_config_data[0], 'enable_private_nodes', False),
                enable_private_endpoint=self._get_known_value(private_cluster_config_data[0], 'enable_private_endpoint', False),
                master_global_access_config=master_global_access_config
            )

        #Metadata and Shielded Instance Config
        metadata = {'disable-legacy-endpoints': 'true'}
        shielded_instance_config = GcpContainerClusterShielededInstanceConfig(False, True)
        workload_metadata_config_mode = GcpContainerClusterWorkloadMetadataConfigMode.MODE_UNSPECIFIED
        if node_config_data := self._get_known_value(attributes, 'node_config'):
            metadata = self._get_known_value(node_config_data[0], 'metadata', {'disable-legacy-endpoints': 'true'})

            if shielded_instance_config_data := self._get_known_value(node_config_data[0], 'shielded_instance_config'):
                shielded_instance_config = GcpContainerClusterShielededInstanceConfig(
                    enable_secure_boot=self._get_known_value(shielded_instance_config_data[0], 'enable_secure_boot', False),
                    enable_integrity_monitoring=self._get_known_value(shielded_instance_config_data[0], 'enable_integrity_monitoring', False))

            # Workload Metadata Config
            if workload_metadata_config_data := self._get_known_value(node_config_data[0], 'workload_metadata_config'):
                workload_metadata_config_mode = enum_implementation(GcpContainerClusterWorkloadMetadataConfigMode, workload_metadata_config_data[0]['mode'])

        # Release Channel
        release_channel = GcpContainerClusterReleaseChannel.REGULAR
        if release_channel_data := self._get_known_value(attributes, 'release_channel'):
            release_channel = enum_implementation(GcpContainerClusterReleaseChannel, release_channel_data[0]['channel'])

        container_cluster = GcpContainerCluster(name, location, cluster_ipv4_cidr,
                                                enable_shielded_nodes, master_authorized_networks_config,
                                                authenticator_groups_config, network_config, private_cluster_config, metadata,
                                                shielded_instance_config, workload_metadata_config_mode, release_channel)
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
