from typing import List, Optional
from cloudrail.knowledge.utils.port_set import PortSet
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource
from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_pool import GcpComputeTargetPool


class GcpComputeForwardingRule(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            target: (Optional) The URL of the target resource to receive the matched traffic.
            port_range: The port range being used to forward traffic to the target.
    """

    def __init__(self,
                 name: str,
                 target: str,
                 port_range: PortSet):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_FORWARDING_RULE)
        self.name: str = name
        self.target: str = target
        self.port_range: PortSet = port_range
        self.target_pool: GcpComputeTargetPool = None

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    @property
    def is_tagable(self) -> bool:
        return False

    @property
    def is_labeled(self) -> bool:
        return True

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/net-services/loadbalancing/list/frontends?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Forwarding Rule'
        else:
            return 'Compute Forwarding Rules'

    def to_drift_detection_object(self) -> dict:
        return {'target': self.target,
                'port_range': self.port_range.port_ranges,
                'labels': self.labels}
