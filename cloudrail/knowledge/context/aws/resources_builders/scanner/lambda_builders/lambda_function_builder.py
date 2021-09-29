from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_lambda_function


class LambdaFunctionBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'lambda-list-versions-by-function/*'

    def get_section_name(self) -> str:
        return 'Versions'

    def do_build(self, attributes: dict):
        return build_lambda_function(attributes)
