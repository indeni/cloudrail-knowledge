from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_api_gateway_v2_vpc_link
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class ApiGatewayVpcLinkBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_api_gateway_v2_vpc_link(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_APIGATEWAYV_2_VPC_LINK
