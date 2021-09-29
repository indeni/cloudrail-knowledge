from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_cloudwatch_logs_policy_destination
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudWatchLogsDestinationPolicyBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_cloudwatch_logs_policy_destination(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDWATCH_LOG_DESTINATION_POLICY
