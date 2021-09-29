from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_s3_access_point_policy


class S3BucketAccessPointPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 's3control-get-access-point-policy/*'

    def get_section_name(self) -> str:
        return 'Policy'

    def do_build(self, attributes: dict):
        return build_s3_access_point_policy(attributes)
