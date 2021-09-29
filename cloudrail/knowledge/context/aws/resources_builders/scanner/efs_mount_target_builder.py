from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_efs_mount_target_base, build_efs_mount_target_security_groups


class EfsMountTargetBaseBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'efs-describe-mount-targets/*'

    def get_section_name(self) -> str:
        return 'MountTargets'

    def do_build(self, attributes: dict):
        return build_efs_mount_target_base(attributes)


class EfsMountTargetSecurityGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'efs-describe-mount-target-security-groups/*'

    def get_section_name(self) -> str:
        return ''

    def do_build(self, attributes: dict):
        return build_efs_mount_target_security_groups(attributes)
