from abc import abstractmethod
from typing import List
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_user_assigned_identity import AzureAssignedUserIdentity
from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class BaseAssignedUserIdentityBuilder(BaseAzureScannerBuilder):

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    def do_build(self, attributes: dict) -> List[AzureAssignedUserIdentity]:
        managed_identities: List[AzureAssignedUserIdentity] = []
        if 'identity' in attributes:
            for identity_id, identity in attributes['identity'].get('userAssignedIdentities', {}).items():
                managed_identities.append(AzureAssignedUserIdentity(identity_id=identity_id,
                                                                    identity_name=identity_id.split('/')[-1],
                                                                    client_id=identity['clientId'],
                                                                    principal_id=identity['principalId'],
                                                                    tenant_id=attributes['tenant_id']))
        return managed_identities
