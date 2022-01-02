from typing import Dict, Optional, List
from cloudrail.knowledge.context.aws.cloudformation.cloudformation_constants import CloudformationResourceType
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket import S3Bucket
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_encryption import S3BucketEncryption
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_logging import S3BucketLogging
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_versioning import S3BucketVersioning
from cloudrail.knowledge.context.aws.resources.s3.s3_acl import S3ACL, GranteeTypes, S3Permission, S3PredefinedGroups
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationS3BucketBuilder(BaseCloudformationBuilder):

    def __init__(self, cfn_by_type_map: Dict[CloudformationResourceType, Dict[str, Dict]]) -> None:
        super().__init__(CloudformationResourceType.S3_BUCKET, cfn_by_type_map)

    def parse_resource(self, cfn_res_attr: dict) -> S3Bucket:
        bucket_name: str = self._get_bucket_name(cfn_res_attr)
        return S3Bucket(account=cfn_res_attr['account_id'],
                        bucket_name=bucket_name,
                        arn='arn:aws:s3:::{}'.format(bucket_name),
                        region=cfn_res_attr['region'],
                        policy=None)

    @classmethod
    def _get_bucket_name(cls, cfn_res_attr: dict) -> str:
        return cls.get_property(cfn_res_attr['Properties'], 'BucketName', cls.get_resource_id(cfn_res_attr))


class CloudformationS3BucketEncryptionBuilder(CloudformationS3BucketBuilder):

    def parse_resource(self, cfn_res_attr: dict) -> S3BucketEncryption:
        properties: dict = cfn_res_attr['Properties']
        bucket_name: str = self._get_bucket_name(cfn_res_attr)
        return S3BucketEncryption(bucket_name=bucket_name,
                                  encrypted='BucketEncryption' in properties,
                                  region=cfn_res_attr['region'],
                                  account=cfn_res_attr['account_id'])


class CloudformationS3BucketVersioningBuilder(CloudformationS3BucketBuilder):

    def parse_resource(self, cfn_res_attr: dict) -> S3BucketVersioning:
        properties: dict = cfn_res_attr['Properties']
        bucket_name: str = self._get_bucket_name(cfn_res_attr)
        return S3BucketVersioning(bucket_name=bucket_name,
                                  versioning=self.get_property(properties.get('VersioningConfiguration', {}), 'Status') == 'Enabled',
                                  account=cfn_res_attr['account_id'],
                                  region=cfn_res_attr['region'])


class CloudformationS3BucketLoggingBuilder(CloudformationS3BucketBuilder):

    def parse_resource(self, cfn_res_attr: dict) -> Optional[S3BucketLogging]:
        res_properties: dict = cfn_res_attr['Properties']
        if 'LoggingConfiguration' in res_properties:
            bucket_name: str = self._get_bucket_name(cfn_res_attr)
            destination_bucket = self.get_property(res_properties['LoggingConfiguration'], 'DestinationBucketName')
            log_file_prefix = self.get_property(res_properties['LoggingConfiguration'], 'LogFilePrefix')
            return S3BucketLogging(bucket_name,
                                   destination_bucket,
                                   log_file_prefix,
                                   cfn_res_attr['account_id'],
                                   cfn_res_attr['region'])
        else:
            return None

class CloudformationS3BucketAclBuilder(CloudformationS3BucketBuilder):

    def parse_resource(self, cfn_res_attr: dict) -> List[S3ACL]:
        properties: dict = cfn_res_attr['Properties']
        if canned_acl := self.get_property(properties, 'AccessControl'):
            bucket_name = self._get_bucket_name(cfn_res_attr)
            region = cfn_res_attr['region']
            account = cfn_res_attr['account_id']
            if canned_acl == 'PublicRead':
                return [S3ACL(S3Permission['READ'], GranteeTypes.GROUP, S3PredefinedGroups.ALL_USERS.value, bucket_name, account, region)]
            if canned_acl == 'PublicReadWrite':
                return [S3ACL(S3Permission['READ'], GranteeTypes.GROUP, S3PredefinedGroups.ALL_USERS.value, bucket_name, account, region),
                        S3ACL(S3Permission['WRITE'], GranteeTypes.GROUP, S3PredefinedGroups.ALL_USERS.value, bucket_name, account, region)]
            if canned_acl == 'AuthenticatedRead':
                return [S3ACL(S3Permission['READ'], GranteeTypes.GROUP, S3PredefinedGroups.AUTHENTICATED_USERS.value, bucket_name, account, region)]
            if canned_acl == 'LogDeliveryWrite':
                return [S3ACL(S3Permission['WRITE'], GranteeTypes.GROUP, S3PredefinedGroups.LOG_DELIVERY.value, bucket_name, account, region),
                        S3ACL(S3Permission['READ_ACP'], GranteeTypes.GROUP, S3PredefinedGroups.LOG_DELIVERY.value, bucket_name, account, region)]
        return []
