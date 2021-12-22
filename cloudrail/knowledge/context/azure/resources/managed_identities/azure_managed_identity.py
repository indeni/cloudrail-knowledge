from enum import Enum


class ManagedIdentityType(Enum):
    SYSTEM_ASSIGNED = 'SystemAssigned'
    USER_ASSIGNED = 'UserAssigned'


class AzureManagedIdentity:

    def __init__(self, principal_id: str, tenant_id: str, identity_type: ManagedIdentityType= ManagedIdentityType.SYSTEM_ASSIGNED) -> None:
        super().__init__()
        self.principal_id: str = principal_id
        self.tenant_id: str = tenant_id
        self.identity_type: ManagedIdentityType = identity_type

    def to_drift_detection_object(self) -> dict:
        return {'principal_id': self.principal_id,
                'tenant_id': self.tenant_id,
                'identity_type': self.identity_type,
                }
