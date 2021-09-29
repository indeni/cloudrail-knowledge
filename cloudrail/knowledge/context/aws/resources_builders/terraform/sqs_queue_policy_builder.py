from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_sqs_queue_policy


class SqsQueuePolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_sqs_queue_policy(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_SQS_QUEUE_POLICY
