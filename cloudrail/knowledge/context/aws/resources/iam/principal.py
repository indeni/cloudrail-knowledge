from dataclasses import dataclass
from enum import Enum
from typing import List


class PrincipalType(Enum):
    NO_PRINCIPAL = "NoPrincipal"
    AWS = "AWS"
    PUBLIC = "Public"
    IGNORED = "Ignored"
    SERVICE = "Service"
    FEDERATED = "Federated"
    CANONICAL_USER = "CanonicalUser"


@dataclass
class Principal:
    principal_type: PrincipalType  # todo - should be a map
    principal_values: List[str]

    def to_dict(self):
        return {'principal_type': self.principal_type.value,
                'principal_values': self.principal_values}
