from abc import abstractmethod
from typing import Optional, List

from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.mergeable import Mergeable


class AzureResource(Mergeable):

    def __init__(self, resource_type: AzureResourceType):
        super().__init__()
        self.subscription_id: str = None
        self.resource_group_name: Optional[str] = None
        self.location: str = None
        self.tf_resource_type: AzureResourceType = resource_type
        self.tenant_id: str = None
        self._id: str = None

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    def get_friendly_name(self) -> str:
        if self.iac_state:
            return self.iac_state.address
        return self.get_name() or self.get_id()

    @property
    @abstractmethod
    def is_tagable(self) -> bool:
        pass

    def get_id(self) -> str:
        return self._id

    def set_id(self, _id: str):
        if _id:
            self._id = _id
            self.with_aliases(_id)
