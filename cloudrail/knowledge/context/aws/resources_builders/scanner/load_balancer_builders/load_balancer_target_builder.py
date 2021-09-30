import os
import urllib

from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_load_balancer_target


class LoadBalancerTargetBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'elbv2-describe-target-health/*'

    def get_section_name(self) -> str:
        return 'TargetHealthDescriptions'

    def do_build(self, attributes: dict):
        raw_target_group_arn = os.path.basename(attributes['FilePath']).replace('TargetGroupArn-', '').replace('.json', '')
        target_group_arn = urllib.parse.unquote(raw_target_group_arn)
        attributes['TargetGroupArn'] = target_group_arn
        return build_load_balancer_target(attributes)
