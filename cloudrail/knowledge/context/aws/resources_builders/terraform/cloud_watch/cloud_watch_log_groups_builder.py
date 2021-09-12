from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_cloud_watch_log_groups
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudWatchLogGroupsBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_cloud_watch_log_groups(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_CLOUDWATCH_LOG_GROUP
