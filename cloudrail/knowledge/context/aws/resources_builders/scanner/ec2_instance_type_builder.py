from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_ec2_instance_type


class Ec2InstanceTypeBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-instance-types.json'

    def get_section_name(self) -> str:
        return 'InstanceTypes'

    def do_build(self, attributes: dict):
        return build_ec2_instance_type(attributes)
