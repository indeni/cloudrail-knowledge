from abc import abstractmethod
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_user_assigned_identity import AzureAssignedUserIdentity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AssignedUserIdentityBuilder(BaseAzureScannerBuilder):

    @abstractmethod
    def get_file_name(self) -> str:
        return 'list-user-identities.json'

    def do_build(self, attributes: dict) -> AzureAssignedUserIdentity:
        properties = attributes['properties']
        return AzureAssignedUserIdentity(identity_name=attributes['name'],
                                         client_id=properties['clientId'],
                                         principal_id=properties['principalId'],
                                         tenant_id=properties['tenantId'])
