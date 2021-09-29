from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_cloudfront_distribution_list, build_cloudfront_distribution_logging
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudFrontDistributionListBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_cloudfront_distribution_list(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDFRONT_DISTRIBUTION_LIST


class CloudfrontDistributionLoggingBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_cloudfront_distribution_logging(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDFRONT_DISTRIBUTION_LIST
