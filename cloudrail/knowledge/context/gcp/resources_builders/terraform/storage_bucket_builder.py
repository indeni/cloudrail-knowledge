from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucket, GcpStorageBucketStorageClass
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder


class StorageBucketBuilder(BaseGcpTerraformBuilder):

    def do_build(self, attributes: dict) -> GcpStorageBucket:
        name: str = attributes.get('name')
        storage_class: GcpStorageBucketStorageClass = GcpStorageBucketStorageClass(attributes.get('storage_class', 'STANDARD'))
        uniform_bucket_level_access: bool = self._get_known_value(attributes, 'uniform_bucket_level_access', False)
        region: str = attributes.get('location')
        logging_enable: bool = len(attributes['logging']) > 0
        return GcpStorageBucket(name=name, storage_class=storage_class,
                                uniform_bucket_level_access=uniform_bucket_level_access,
                                region=region, logging_enable=logging_enable)

    def get_service_name(self) -> GcpResourceType:
        return GcpResourceType.GOOGLE_STORAGE_BUCKET
