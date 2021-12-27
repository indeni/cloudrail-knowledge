from abc import abstractmethod
from typing import List
from cloudrail.knowledge.context.azure.resources.managed_identities.azure_managed_identity import AzureManagedIdentity


class IManagedIdentityResource:

    @abstractmethod
    def get_managed_identities(self) -> List[AzureManagedIdentity]:
        pass

    @abstractmethod
    def get_managed_identities_ids(self) -> List[str]:
        pass
