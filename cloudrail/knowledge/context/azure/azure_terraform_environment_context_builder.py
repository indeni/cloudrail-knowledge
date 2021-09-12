from typing import Type, Optional

from cloudrail.knowledge.context.azure.azure_environment_context_enrichment import AzureEnvironmentContextEnrichment
from cloudrail.knowledge.context.azure.scanner.azure_scanner_context_builder import AzureScannerContextBuilder
from cloudrail.knowledge.context.azure.terraform.azure_terraform_context_builder import AzureTerraformContextBuilder
from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_defaults_merger import EnvironmentContextDefaultsMerger
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder


class AzureTerraformEnvironmentContextBuilder(BaseEnvironmentContextBuilder):

    @classmethod
    def get_default_account_id(cls) -> str:
        return '00000000-0000-0000-0000-000000000000'

    @classmethod
    def get_scanner_builder_type(cls) -> Type[ScannerContextBuilder]:
        return AzureScannerContextBuilder

    @classmethod
    def get_iac_builder_type(cls) -> Type[IacContextBuilder]:
        return AzureTerraformContextBuilder

    @classmethod
    def get_defaults_merger_type(cls) -> Optional[Type[EnvironmentContextDefaultsMerger]]:
        return None

    @classmethod
    def get_context_enrichment_type(cls) -> Type[EnvironmentContextEnrichment]:
        return AzureEnvironmentContextEnrichment
