from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_main_route_table_association
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class MainRouteTableAssociationsBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_main_route_table_association(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_MAIN_ROUTE_TABLE_ASSOCIATION
