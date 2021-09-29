from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_load_balancer_attributes


class LoadBalancerAttributesBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'elbv2-describe-load-balancer-attributes/*'

    def get_section_name(self) -> str:
        return ''

    def do_build(self, attributes: dict):
        return build_load_balancer_attributes(attributes)
