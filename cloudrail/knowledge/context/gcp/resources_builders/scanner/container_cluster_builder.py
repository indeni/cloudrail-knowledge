from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfig,\
    GcpContainerMasterAuthNetConfigCidrBlk, GcpContainerClusterAuthGrpConfig, GcpContainerClusterNetworkPolicy, GcpContainerClusterNetworkConfigProvider, \
    GcpContainerClusterPrivateClusterConfig, GcpContainerClusterShielededInstanceConfig, GcpContainerClusterWorkloadMetadataConfigMode, \
    GcpContainerClusterReleaseChannel, GcpContainerClusterNodeConfig, GcpContainerClusterNetworkingMode
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
        node_config = attributes['nodeConfig']
        enable_shielded_nodes = bool(attributes.get("shieldedNodes", {}).get("enabled"))
        master_authorized_networks_config_dict = attributes.get("masterAuthorizedNetworksConfig")
        master_authorized_networks_config = self.build_master_authorized_networks_config(master_authorized_networks_config_dict) if master_authorized_networks_config_dict else None
        authenticator_groups_config_dict = attributes.get("authenticatorGroupsConfig")
        authenticator_groups_config = GcpContainerClusterAuthGrpConfig(authenticator_groups_config_dict.get("securityGroup")) if authenticator_groups_config_dict else None

        ## Network Config
        network_policy = GcpContainerClusterNetworkPolicy(GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED, False)
        if network_policy_data := attributes.get('networkPolicy'):
            network_policy = GcpContainerClusterNetworkPolicy(
                provider=enum_implementation(GcpContainerClusterNetworkConfigProvider,
                                             network_policy_data.get('provider'),  GcpContainerClusterNetworkConfigProvider.PROVIDER_UNSPECIFIED),
                enabled=network_policy_data.get('enabled', False))

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

        # Service Account
        service_account = node_config['serviceAccount']
        node_config = GcpContainerClusterNodeConfig(metadata=metadata, shielded_instance_config=shielded_instance_config,
                                                    workload_metadata_config_mode=workload_metadata_config_mode, service_account=service_account)
        # Release Channel
        release_channel = enum_implementation(GcpContainerClusterReleaseChannel, attributes['releaseChannel']['channel'])

        # Issue Client Certificate
        issue_client_certificate = attributes.get('masterAuth', {}).get('clientCertificateConfig', {}).get('issueClientCertificate') or \
                                   bool(attributes.get('masterAuth', {}).get('clientCertificate'))

        # Pod security policy config
        pod_security_policy_enabled = attributes.get('podSecurityPolicyConfig', {}).get('enabled', False)

        # Binary Auth
        enable_binary_authorization = attributes.get('binaryAuthorization', {}).get('enabled', False)

        # Networking Mode
        networking_mode = GcpContainerClusterNetworkingMode.VPC_NATIVE if attributes.get('ipAllocationPolicy', {}).get('useIpAliases') else \
                          GcpContainerClusterNetworkingMode.ROUTES
        container_cluster = GcpContainerCluster(name, location, cluster_ipv4_cidr, enable_shielded_nodes, master_authorized_networks_config,
                                                authenticator_groups_config, network_policy, private_cluster_config, node_config, release_channel,
                                                issue_client_certificate, pod_security_policy_enabled, enable_binary_authorization, networking_mode)
        container_cluster.labels = get_gcp_labels(attributes.get("resourceLabels"), attributes['salt'])

        return container_cluster

    @staticmethod
    def build_master_authorized_networks_config(master_authorized_networks_config: dict) -> GcpContainerMasterAuthNetConfig:
        cidr_blocks_list = master_authorized_networks_config.get("cidrBlocks", [])
        cidr_blocks = [GcpContainerMasterAuthNetConfigCidrBlk(cidr_block.get("cidrBlock"), cidr_block.get("displayName")) for cidr_block in cidr_blocks_list]

        return GcpContainerMasterAuthNetConfig(cidr_blocks)
