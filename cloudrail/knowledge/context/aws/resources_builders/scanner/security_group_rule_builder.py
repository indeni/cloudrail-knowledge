from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import \
    build_security_group_rules


class SecurityGroupRuleBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-security-groups.json'

    def get_section_name(self) -> str:
        return 'SecurityGroups'

    def do_build(self, attributes: dict):
        return build_security_group_rules(attributes)
