from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder \
    import build_auto_scaling_group


class AutoScalingGroupBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'autoscaling-describe-auto-scaling-groups.json'

    def get_section_name(self) -> str:
        return 'AutoScalingGroups'

    def do_build(self, attributes: dict):
        return build_auto_scaling_group(attributes)
