from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_internet_gateway
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway


class InternetGatewayBuilder(AwsTerraformBuilder):

    def do_build(self, attributes) -> InternetGateway:
        attributes["igw_type"] = IgwType.IGW
        attributes["tf_res_type"] = self.get_service_name()
        return build_internet_gateway(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_INTERNET_GATEWAY
