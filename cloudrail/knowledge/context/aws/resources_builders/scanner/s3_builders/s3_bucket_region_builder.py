import os

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources.s3.s3_bucket_regions import S3BucketRegions


class S3BucketRegionBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 's3-get-bucket-location/*'

    def get_section_name(self) -> str:
        return 'LocationConstraint'

    def do_build(self, attributes: dict):
        bucket_name = os.path.basename(attributes['FilePath'])
        region = attributes['Value']
        # If the region is None (null in the json), then the region defaults to us-east-1
        # This is according to the documentation in https://docs.aws.amazon.com/cli/latest/reference/s3api/get-bucket-location.html
        # At the 'Output' section
        return S3BucketRegions(bucket_name, region or 'us-east-1')
