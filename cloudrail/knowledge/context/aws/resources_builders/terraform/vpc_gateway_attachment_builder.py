from cloudrail.knowledge.context.aws.resources.ec2.vpc_gateway_attachment import VpcGatewayAttachment
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_vpc_gateway_attachment


class VpcGatewayAttachmentBuilder(AwsTerraformBuilder):

    def do_build(self, attributes) -> VpcGatewayAttachment:
        attributes["igw_type"] = IgwType.IGW
        attributes["tf_res_type"] = self.get_service_name()
        return build_vpc_gateway_attachment(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_INTERNET_GATEWAY
