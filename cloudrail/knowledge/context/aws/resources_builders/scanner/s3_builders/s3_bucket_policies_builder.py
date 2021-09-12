import json
import os

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_s3_policy


class S3BucketPoliciesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 's3-get-bucket-policy/*'

    def get_section_name(self) -> str:
        return 'Policy'

    def do_build(self, attributes: dict):
        bucket_name = os.path.basename(attributes['FilePath']).replace('Bucket-', '').replace('.json', '')
        policy_data = json.loads(attributes['Value'])
        policy_data['BucketName'] = bucket_name
        return build_s3_policy(policy_data, attributes)
