from dataclasses import dataclass
import dataclasses
from typing import Optional, List

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


@dataclass
class GcpComputeSubNetworkLogConfig:
    """
        Attributes:
        enabled: Indication if the flow logs are enabled or not.
        aggregation_interval: (Optional) Toggles the aggregation interval for collecting flow logs.
        flow_sampling : (Optional) The value of the field must be in [0, 1]. Set the sampling rate of VPC flow logs within the subnetwork
                                   where 1.0 means all collected logs are reported and 0.0 means no logs are reported.
        metadata: (Optional) Configures whether metadata fields should be added to the reported VPC flow logs.
        metadata_fields: (Optional) List of metadata fields that should be added to reported logs.
        filter_expr : (Optional) Export filter used to define which VPC flow logs should be logged, as as CEL expression.
    """
    enabled: bool
    aggregation_interval: str
    flow_sampling: int
    metadata: str
    metadata_fields: List[str]
    filter_expr: str


class GcpComputeSubNetwork(GcpResource):
    """
        Attributes:
        name: (Required) A unique name of the resource.
        subnetwork_id: (Optional) an identifier for the resource
        self_link: (Optional) The URI of the created resource.
        region: (Optional) The GCP region for this subnetwork.
        network_identifier: (Required) The network this subnet belongs to.
        ip_cidr_range: (Required) The range of internal addresses that are owned by this subnetwork.
        log_config: (Optional) Denotes the logging options for the subnetwork flow logs.
    """

    def __init__(self,
                 name: str,
                 subnetwork_id: str,
                 self_link: str,
                 region: str,
                 network_identifier: str,
                 ip_cidr_range: str,
                 log_config: GcpComputeSubNetworkLogConfig):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_SUBNETWORK)
        self.name: str = name
        self.subnetwork_id: str = subnetwork_id
        self.self_link: str = self_link
        self.region: str = region
        self.network_identifier: str = network_identifier
        self.ip_cidr_range: str = ip_cidr_range
        self.log_config: GcpComputeSubNetworkLogConfig = log_config
        self.with_aliases(subnetwork_id, self_link)

    def get_keys(self) -> List[str]:
        return [self.self_link]

    def get_id(self) -> str:
        return self.subnetwork_id

    def get_name(self) -> str:
        return self.name

    @property
    def is_labeled(self) -> bool:
        return False

    @property
    def is_tagable(self) -> bool:
        return False

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/networking/subnetworks/details/{self.region}/{self.name}?project={self.project_id}' if self.region else None

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute SubNetwork Details'  # TODO: check the name

    def to_drift_detection_object(self) -> dict:
        return {"ip_cidr_range": self.ip_cidr_range,
                "log_config": dataclasses.asdict(self.log_config)}
