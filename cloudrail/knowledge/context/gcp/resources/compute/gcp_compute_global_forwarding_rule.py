from typing import List, Optional

from cloudrail.knowledge.context.gcp.resources.compute.gcp_compute_target_proxy import GcpComputeTargetProxy
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeGlobalForwardingRule(GcpResource):
    """
        Attributes:
            name: (Required) A unique name of the resource.
            target_identifier: (Required) The URL of the target resource to receive the matched traffic.
    """

    def __init__(self,
                 name: str,
                 target_identifier: str):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_GLOBAL_FORWARDING_RULE)
        self.name: str = name
        self.target_identifier: str = target_identifier
        self.target: Optional[GcpComputeTargetProxy] = None

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
        return f'{self._BASE_URL}/net-services/loadbalancing/advanced/globalForwardingRules/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Compute Global Forwarding Rule'
        else:
            return 'Compute Global Forwarding Rules'

    def to_drift_detection_object(self) -> dict:
        return {'target': self.target_identifier}
