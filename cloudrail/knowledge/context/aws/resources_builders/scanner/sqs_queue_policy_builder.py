from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_sqs_queue_policy


class SqsQueuePolicyBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'sqs-get-queue-attributes/*'

    def get_section_name(self) -> str:
        return 'Attributes'

    def do_build(self, attributes: dict):
        return build_sqs_queue_policy(attributes)
