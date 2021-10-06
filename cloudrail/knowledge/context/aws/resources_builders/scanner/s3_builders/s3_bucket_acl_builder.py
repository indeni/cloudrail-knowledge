import os

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_s3_acl


class S3BucketAclBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 's3-get-bucket-acl/*'

    def get_section_name(self) -> str:
        return None

    def do_build(self, attributes: dict):
        bucket_name = os.path.basename(attributes['FilePath']).replace('Bucket-', '').replace('.json', '')
        attributes['BucketName'] = bucket_name
        return build_s3_acl(attributes)
