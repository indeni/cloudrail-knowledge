from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_efs_mount_target
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class EfsMountTargetBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_efs_mount_target(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_EFS_MOUNT_TARGET
