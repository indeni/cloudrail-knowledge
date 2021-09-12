from typing import Type, Optional

from cloudrail.knowledge.context.environment_context.base_environment_context_builder import BaseEnvironmentContextBuilder
from cloudrail.knowledge.context.gcp.gcp_environment_context_enrichment import GcpEnvironmentContextEnrichment
from cloudrail.knowledge.context.gcp.scanner.gcp_scanner_context_builder import GcpScannerContextBuilder
from cloudrail.knowledge.context.gcp.terraform.gcp_terraform_context_builder import GcpTerraformContextBuilder
from cloudrail.knowledge.context.environment_context.environment_context_enrichment import EnvironmentContextEnrichment
from cloudrail.knowledge.context.environment_context.environment_context_defaults_merger import EnvironmentContextDefaultsMerger
from cloudrail.knowledge.context.environment_context.iac_context_builder import IacContextBuilder
from cloudrail.knowledge.context.environment_context.scanner_context_builder import ScannerContextBuilder


class GcpTerraformEnvironmentContextBuilder(BaseEnvironmentContextBuilder):

    @classmethod
    def get_default_account_id(cls) -> str:
        return 'no-cloud-account-used'

    @classmethod
    def get_scanner_builder_type(cls) -> Type[ScannerContextBuilder]:
        return GcpScannerContextBuilder

    @classmethod
    def get_iac_builder_type(cls) -> Type[IacContextBuilder]:
        return GcpTerraformContextBuilder

    @classmethod
    def get_defaults_merger_type(cls) -> Optional[Type[EnvironmentContextDefaultsMerger]]:
        return None

    @classmethod
    def get_context_enrichment_type(cls) -> Type[EnvironmentContextEnrichment]:
        return GcpEnvironmentContextEnrichment
