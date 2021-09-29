from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_cloudwatch_logs_policy_destination


class CloudWatchLogsDestinationPolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'logs-describe-destinations.json'

    def get_section_name(self) -> str:
        return 'destinations'

    def do_build(self, attributes: dict):
        return build_cloudwatch_logs_policy_destination(attributes)
