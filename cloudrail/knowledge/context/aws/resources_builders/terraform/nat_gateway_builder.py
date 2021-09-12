from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_nat_gateways
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class NatGatewayBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_nat_gateways(attributes)

    def get_service_name(self) -> str:
        return AwsServiceName.AWS_NAT_GATEWAY
