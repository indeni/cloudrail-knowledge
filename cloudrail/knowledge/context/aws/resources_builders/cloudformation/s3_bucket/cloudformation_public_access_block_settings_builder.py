from typing import Optional
from cloudrail.knowledge.context.aws.resources.s3.public_access_block_settings import PublicAccessBlockSettings, PublicAccessBlockLevel
from cloudrail.knowledge.context.aws.resources_builders.cloudformation.s3_bucket.cloudformation_s3_bucket_builder import CloudformationS3BucketBuilder


class CloudformationPublicAccessBlockSettingsBuilder(CloudformationS3BucketBuilder):

    def parse_resource(self, cfn_res_attr: dict) -> Optional[PublicAccessBlockSettings]:
        properties: dict = cfn_res_attr['Properties']
        bucket_name: str = self.get_property(properties, 'BucketName', self.get_resource_id(cfn_res_attr))

        if 'PublicAccessBlockConfiguration' in properties:
            access_settings: dict = properties['PublicAccessBlockConfiguration']
            return PublicAccessBlockSettings(bucket_name_or_account_id=bucket_name,
                                             block_public_acls=self.get_property(access_settings, "BlockPublicAcls", False),
                                             block_public_policy=self.get_property(access_settings, "BlockPublicPolicy", False),
                                             ignore_public_acls=self.get_property(access_settings, "IgnorePublicAcls", False),
                                             restrict_public_buckets=self.get_property(access_settings, "RestrictPublicBuckets", False),
                                             access_level=PublicAccessBlockLevel.BUCKET,
                                             account=cfn_res_attr['account_id'],
                                             region=cfn_res_attr['region'])
        else:
            return None
