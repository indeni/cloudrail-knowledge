from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucketStorageClass, GcpStorageBucket
from cloudrail.knowledge.context.gcp.resources_builders.scanner.base_gcp_scanner_builder import BaseGcpScannerBuilder


class StorageBucketBuilder(BaseGcpScannerBuilder):

    def get_file_name(self) -> str:
        return 'storage-v1-buckets-list.json'

    def do_build(self, attributes: dict):
        name: str = attributes.get('name')
        storage_class: GcpStorageBucketStorageClass = GcpStorageBucketStorageClass(attributes.get('storageClass', 'STANDARD'))
        uniform_bucket_level_access: bool = attributes.get('iamConfiguration', {})\
            .get('uniformBucketLevelAccess', {}).get('enabled', False)
        region: str = attributes.get('location')
        logging_enable: bool = 'logging' in attributes
        return GcpStorageBucket(name=name, storage_class=storage_class,
                                uniform_bucket_level_access=uniform_bucket_level_access,
                                region=region, logging_enable=logging_enable)
