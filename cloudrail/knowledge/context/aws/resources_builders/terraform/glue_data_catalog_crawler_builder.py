from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_glue_data_catalog_crawler
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class GlueDataCatalogCrawlerBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_glue_data_catalog_crawler(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_GLUE_CRAWLER
