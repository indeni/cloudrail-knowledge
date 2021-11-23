from typing import List, Optional
from enum import Enum
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpStorageBucketStorageClass(Enum):
    STANDARD = 'STANDARD'
    MULTI_REGIONAL = 'MULTI_REGIONAL'
    REGIONAL = 'REGIONAL'
    NEARLINE = 'NEARLINE'
    COLDLINE = 'COLDLINE'
    ARCHIVE = 'ARCHIVE'


class GcpStorageBucket(GcpResource):
    """
        Attributes:
            name: The name of the bucket.
            storage_class: (Optional, Default = 'STANDARD') The Storage Class of the new bucket. Supported values are STANDARD, MULTI_REGIONAL, REGIONAL, NEARLINE, COLDLINE, ARCHIVE.
            uniform_bucket_level_access: (Optional, Default = false) Enables Uniform bucket-level access access to a bucket.
            region: bucket region (geographic location)
    """

    def __init__(self,
                 name: str,
                 storage_class: GcpStorageBucketStorageClass,
                 uniform_bucket_level_access: bool,
                 region: str):

        super().__init__(GcpResourceType.GOOGLE_STORAGE_BUCKET)
        self.name: str = name
        self.storage_class: GcpStorageBucketStorageClass = storage_class
        self.uniform_bucket_level_access: bool = uniform_bucket_level_access
        self.region: str = region
        self.with_aliases(name)

    def get_keys(self) -> List[str]:
        return [self.name]

    @property
    def is_tagable(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.name

    def get_name(self) -> Optional[str]:
        return self.name

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/storage/browser/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Storage Bucket'
        else:
            return 'Storage Buckets'

    @property
    def is_labeled(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {
            'name': self.name,
            'storage_class': self.storage_class,
            'uniform_bucket_level_access': self.uniform_bucket_level_access,
            'region': self.region
        }
