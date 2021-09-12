from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_s3_bucket_versioning


class S3BucketVersioningBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 's3-get-bucket-versioning/*'

    def get_section_name(self) -> str:
        pass

    def do_build(self, attributes: dict):
        return build_s3_bucket_versioning(attributes)
