from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_mq_broker


class MqBrokerBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_mq_broker(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_MQ_BROKER
