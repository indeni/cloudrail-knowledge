from cloudrail.knowledge.context.gcp.resources.cluster.gcp_container_cluster import GcpContainerCluster, GcpContainerMasterAuthNetConfig, GcpContainerMasterAuthNetConfigCidrBlk, \
    GcpContainerClusterAuthGrpConfig
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder
from cloudrail.knowledge.utils.tags_utils import get_gcp_labels


class ContainerClusterBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'container-v1-projects_zones_clusters-list.json'

    def do_build(self, attributes: dict) -> GcpContainerCluster:
        name = attributes["name"]
        location = attributes.get("location")
        cluster_ipv4_cidr = attributes.get("clusterIpv4Cidr")
        enable_shielded_nodes = bool(attributes.get("shieldedNodes", {}).get("enabled"))
        master_authorized_networks_config_dict = attributes.get("masterAuthorizedNetworksConfig")
        master_authorized_networks_config = self.build_master_authorized_networks_config(master_authorized_networks_config_dict) if master_authorized_networks_config_dict else None
        authenticator_groups_config_dict = attributes.get("authenticatorGroupsConfig")
        authenticator_groups_config = GcpContainerClusterAuthGrpConfig(authenticator_groups_config_dict.get("securityGroup")) if authenticator_groups_config_dict else None

        container_cluster = GcpContainerCluster(name, location, cluster_ipv4_cidr, enable_shielded_nodes, master_authorized_networks_config, authenticator_groups_config)
        container_cluster.labels = get_gcp_labels(attributes.get("resourceLabels"), attributes['salt'])

        return container_cluster

    @staticmethod
    def build_master_authorized_networks_config(master_authorized_networks_config: dict) -> GcpContainerMasterAuthNetConfig:
        cidr_blocks_list = master_authorized_networks_config.get("cidrBlocks", [])
        cidr_blocks = [GcpContainerMasterAuthNetConfigCidrBlk(cidr_block.get("cidrBlock"), cidr_block.get("displayName")) for cidr_block in cidr_blocks_list]

        return GcpContainerMasterAuthNetConfig(cidr_blocks)
