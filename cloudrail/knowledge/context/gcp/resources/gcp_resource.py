from abc import abstractmethod
from typing import List, Optional, Dict

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.mergeable import Mergeable


class GcpResource(Mergeable):
    _BASE_URL = 'https://console.cloud.google.com/'

    def __init__(self, resource_type: GcpResourceType):
        super().__init__()
        self.tf_resource_type: GcpResourceType = resource_type
        self.project_id: str = None
        self.tags: Optional[List[str]] = None
        self.labels: Optional[Dict[str, str]] = None

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    def get_friendly_name(self) -> str:
        if self.iac_state:
            return self.iac_state.address
        return self.get_name() or self.get_id()

    @property
    @abstractmethod
    def is_tagable(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_labeled(self) -> bool:
        pass
