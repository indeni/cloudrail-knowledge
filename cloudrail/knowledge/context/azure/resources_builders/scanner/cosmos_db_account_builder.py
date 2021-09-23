from cloudrail.knowledge.context.azure.resources.databases.azure_cosmos_db_account import AzureCosmosDBAccount

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class CosmosDBAccountBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'cosmos_db_account.json'

    def do_build(self, attributes: dict) -> AzureCosmosDBAccount:
        return None
