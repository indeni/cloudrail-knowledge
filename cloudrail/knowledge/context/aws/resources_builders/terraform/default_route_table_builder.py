from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_default_route_table
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class DefaultRouteTableBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_default_route_table(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_DEFAULT_ROUTE_TABLE
