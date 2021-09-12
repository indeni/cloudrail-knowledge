from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_cloudfront_distribution_list, build_cloudfront_distribution_logging


class CloudFrontDistributionListBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'cloudfront-list-distributions.json'

    def get_section_name(self) -> str:
        return 'DistributionList'

    def do_build(self, attributes: dict):
        return build_cloudfront_distribution_list(attributes)


class CloudfrontDistributionLoggingBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'cloudfront-get-distribution/*'

    def get_section_name(self) -> str:
        return 'Distribution'

    def do_build(self, attributes: dict):
        return build_cloudfront_distribution_logging(attributes)
