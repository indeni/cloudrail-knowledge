from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_dynamodb_table


class DynamoDbBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'dynamodb-describe-table/*'

    def get_section_name(self) -> str:
        return 'Table'

    def do_build(self, attributes: dict):
        return build_dynamodb_table(attributes)
