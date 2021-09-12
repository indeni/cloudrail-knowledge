from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_kinesis_stream


class KinesisStreamBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'kinesis-describe-stream/*'

    def get_section_name(self) -> str:
        return 'StreamDescription'

    def do_build(self, attributes: dict):
        return build_kinesis_stream(attributes)
