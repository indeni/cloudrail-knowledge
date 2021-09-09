from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_kinesis_firehose_stream


class KinesisFirehoseStreamBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'firehose-describe-delivery-stream/*'

    def get_section_name(self) -> str:
        return 'DeliveryStreamDescription'

    def do_build(self, attributes: dict):
        return build_kinesis_firehose_stream(attributes)