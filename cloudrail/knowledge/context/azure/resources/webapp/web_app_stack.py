from typing import Optional, List
from packaging.version import Version
from cloudrail.knowledge.context.azure.resources.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.resources.constants.azure_resource_type import AzureResourceType


class WebAppStack(AzureResource):
    """
        Attributes:
            name: The name of framework.
            preferred_os: OS type (Linux|Win).
            major_version: major framework version.
            minor_versions: minor framework versions list.
    """
    def __init__(self, name: str, preferred_os: str, major_version: int, minor_versions: List[Version]):
        super().__init__(AzureResourceType.NONE)
        self.name: str = name
        self.preferred_os: str = preferred_os
        self.major_version: int = major_version
        self.minor_versions: List[Version] = minor_versions
        self.with_aliases(self.name)

    def get_keys(self) -> List[str]:
        return [self.get_name()]

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {}

    def get_latest_version(self) -> str:
        latest_version: Version = self.minor_versions[0]
        for index in range(1, len(self.minor_versions)):
            if latest_version < self.minor_versions[index]:
                latest_version = self.minor_versions[index]
        return '.'.join([str(num) for num in latest_version.release[:2]]) if len(latest_version.release) > 1 else latest_version.base_version
