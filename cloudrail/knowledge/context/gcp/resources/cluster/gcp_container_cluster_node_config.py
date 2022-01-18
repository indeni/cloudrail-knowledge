from dataclasses import dataclass
from enum import Enum

class GcpClusterDiskType(str, Enum):
    PD_STANDARD = 'pd-standard'
    PD_BALANCED = 'pd-balanced'
    PD_SSD = 'pd-ssd'


class GcpContainerClusterWorkloadMetadataConfigMode(str, Enum):
    MODE_UNSPECIFIED = None
    GCE_METADATA = 'GCE_METADATA'
    GKE_METADATA = 'GKE_METADATA'


@dataclass
class GcpContainerClusterShielededInstanceConfig:
    """
        Attributes:
            enable_secure_boot: (Optional) Indication whether the instance has Secure Boot enabled.
            enable_integrity_monitoring: (Optional) Indication whether the instance has integrity monitoring enabled.
    """
    enable_secure_boot: bool
    enable_integrity_monitoring: bool

@dataclass
class GcpContainerClusterNodeConfig:
    """
        Attributes:
            metadata: (Optional) A metadata Key/Value pairs assigned to an instance in the cluster.
            shielded_instance_config: (Optional) Shielded Instance configurations.
            workload_metadata_config_mode: (Optional) How to expose the node metadata to the workload running on the node.
            service_account: (Optional) The service account to be used by the Node VMs.
            disk_size_gb: (Optional) Size of the disk attached to each node, specified in gb.
            disk_type: (Optional) Type of the disk attached to each node. Options are pd-standard, pd-balanced or pd-ssd.
            gcfs_enabled: (Optional) Whether or not the Google Container Filesystem (GCFS) is enabled.
            image_type: (Optional) The image type to use for this node.
            machine_type: (Optional) The name of a google compute engine machine type.
    """
    def __init__(self,
                 metadata: dict,
                 shielded_instance_config: GcpContainerClusterShielededInstanceConfig,
                 workload_metadata_config_mode: GcpContainerClusterWorkloadMetadataConfigMode,
                 service_account: str,
                 disk_size_gb: int,
                 disk_type: GcpClusterDiskType,
                 gcfs_enabled: bool,
                 image_type: str,
                 machine_type: str):

        self.metadata: dict = metadata
        self.shielded_instance_config: GcpContainerClusterShielededInstanceConfig = shielded_instance_config
        self.workload_metadata_config_mode: GcpContainerClusterWorkloadMetadataConfigMode = workload_metadata_config_mode
        self.service_account: str = service_account
        self.disk_size_gb: int = disk_size_gb
        self.disk_type: GcpClusterDiskType = disk_type
        self.gcfs_enabled: bool = gcfs_enabled
        self.image_type: str = image_type
        self.machine_type: str = machine_type
