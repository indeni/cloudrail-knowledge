from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfig,\
    GcpContainerMasterAuthNetConfigCidrBlk, GcpContainerClusterAuthGrpConfig, GcpContainerClusterNetworkConfig, GcpContainerClusterNetworkConfigProvider, \
    GcpContainerClusterPrivateClusterConfig, GcpContainerClusterShielededInstanceConfig, GcpContainerClusterWorkloadMetadataConfigMode, \
    GcpContainerClusterReleaseChannel
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.utils.tags_utils import get_gcp_labels
from cloudrail.knowledge.utils.enum_utils import enum_implementation


class ContainerClusterBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'container-v1-projects_zones_clusters-list.json'

    def do_build(self, attributes: dict) -> GcpContainerCluster:
        name = attributes["name"]
        location = attributes.get("location")
        cluster_ipv4_cidr = attributes.get("clusterIpv4Cidr")
        node_config = attributes.get('nodeConfig', {})
        enable_shielded_nodes = bool(attributes.get("shieldedNodes", {}).get("enabled"))
        master_authorized_networks_config_dict = attributes.get("masterAuthorizedNetworksConfig")
        master_authorized_networks_config = self.build_master_authorized_networks_config(master_authorized_networks_config_dict) if master_authorized_networks_config_dict else None
        authenticator_groups_config_dict = attributes.get("authenticatorGroupsConfig")
        authenticator_groups_config = GcpContainerClusterAuthGrpConfig(authenticator_groups_config_dict.get("securityGroup")) if authenticator_groups_config_dict else None

        ## Network Config
        network_config = GcpContainerClusterNetworkConfig(GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED, False)
        if network_config_data := attributes.get('networkPolicy'):
            network_config = GcpContainerClusterNetworkConfig(
                provider=enum_implementation(GcpContainerClusterNetworkConfigProvider,
                                             network_config_data.get('provider'),  GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED),
                enabled=network_config_data.get('enabled', False))

        ## Private cluster config
        private_cluster_config = None
        if private_cluster_config_data := attributes.get('privateClusterConfig'):
            master_global_access_config = False
            if master_global_access_config_data := private_cluster_config_data.get('masterGlobalAccessConfig'):
                master_global_access_config = master_global_access_config_data.get('enabled', False)
            private_cluster_config = GcpContainerClusterPrivateClusterConfig(
                enable_private_nodes=private_cluster_config_data.get('enablePrivateNodes', False),
                enable_private_endpoint=private_cluster_config_data.get('enablePrivateEndpoint', False),
                master_global_access_config=master_global_access_config
            )

        ## Metadata
        metadata = node_config.get('metadata')

        # Shielded Instance Config
        shielded_instance_config = GcpContainerClusterShielededInstanceConfig(False, True)
        if shielded_instance_config_data := node_config.get('shieldedInstanceConfig'):
            shielded_instance_config = GcpContainerClusterShielededInstanceConfig(
                enable_secure_boot=shielded_instance_config_data.get('enableSecureBoot', False),
                enable_integrity_monitoring=shielded_instance_config_data.get('enableIntegrityMonitoring', True))

        # Workload Metadata Config
        workload_metadata_config_mode = GcpContainerClusterWorkloadMetadataConfigMode.MODE_UNSPECIFIED
        if workload_metadata_config_data := node_config.get('workloadMetadataConfig'):
            workload_metadata_config_mode = enum_implementation(GcpContainerClusterWorkloadMetadataConfigMode, workload_metadata_config_data['mode'])

        # Release Channel
        release_channel = enum_implementation(GcpContainerClusterReleaseChannel, attributes['releaseChannel']['channel'])

        container_cluster = GcpContainerCluster(name, location, cluster_ipv4_cidr, enable_shielded_nodes,
                                                master_authorized_networks_config, authenticator_groups_config, network_config, private_cluster_config, metadata,
                                                shielded_instance_config, workload_metadata_config_mode, release_channel)
        container_cluster.labels = get_gcp_labels(attributes.get("resourceLabels"), attributes['salt'])

        return container_cluster

    @staticmethod
    def build_master_authorized_networks_config(master_authorized_networks_config: dict) -> GcpContainerMasterAuthNetConfig:
        cidr_blocks_list = master_authorized_networks_config.get("cidrBlocks", [])
        cidr_blocks = [GcpContainerMasterAuthNetConfigCidrBlk(cidr_block.get("cidrBlock"), cidr_block.get("displayName")) for cidr_block in cidr_blocks_list]

        return GcpContainerMasterAuthNetConfig(cidr_blocks)
