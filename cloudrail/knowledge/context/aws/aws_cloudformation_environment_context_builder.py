from typing import Type, Optional
from cloudrail.knowledge.context.aws.aws_environment_context_defaults_merger import AwsEnvironmentContextDefaultsMerger
from cloudrail.knowledge.context.aws.aws_environment_context_enrichment import AwsEnvironmentContextEnrichment
from cloudrail.knowledge.context.aws.cloudformation.aws_cloudformation_context_builder import AwsCloudformationContextBuilder
from cloudrail.knowledge.context.aws.scanner.aws_scanner_context_builder import AwsScannerContextBuilder
from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_defaults_merger import EnvironmentContextDefaultsMerger
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder


class AwsCloudformationEnvironmentContextBuilder(BaseEnvironmentContextBuilder):

    @classmethod
    def get_default_account_id(cls) -> str:
        return '000000000000'

    @classmethod
    def get_scanner_builder_type(cls) -> Type[ScannerContextBuilder]:
        return AwsScannerContextBuilder

    @classmethod
    def get_iac_builder_type(cls) -> Type[IacContextBuilder]:
        return AwsCloudformationContextBuilder

    @classmethod
    def get_defaults_merger_type(cls) -> Optional[Type[EnvironmentContextDefaultsMerger]]:
        return AwsEnvironmentContextDefaultsMerger

    @classmethod
    def get_context_enrichment_type(cls) -> Type[EnvironmentContextEnrichment]:
        return AwsEnvironmentContextEnrichment
