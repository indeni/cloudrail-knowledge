from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import \
    build_launch_configuration, build_auto_scaling_group
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class LaunchConfigurationBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_launch_configuration(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_LAUNCH_CONFIGURATION


class AutoScalingGroupBuilder(AwsTerraformBuilder):

    def do_build(self, attributes):
        return build_auto_scaling_group(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_AUTO_SCALING_GROUP
