# from cloudrail.knowledge.context.azure.resources.databases.azure_cosmos_db_account import AzureCosmosDBAccount
#
# from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder
#
#
# class AzureCosmosDBAccountBuilder(BaseAzureScannerBuilder):
#
#     def get_file_name(self) -> str:
#         return 'cosmos_db_account.json'
#
#     def do_build(self, attributes: dict) -> AzureCosmosDBAccount:
#             return AzureCosmosDBAccount(name=attributes['name'],
#                                    https_only=attributes['properties']['httpsOnly'],
#                                    client_cert_required=attributes['properties'].get('clientCertEnabled', False))
#         return None
