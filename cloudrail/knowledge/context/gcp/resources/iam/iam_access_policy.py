from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpIamPolicyType(str, Enum):
    """
    Attributes:
        Authoritative: Indicate the policy will replace any existing policies.
        Role-authoritative: Indicate the policy will grant a role to specific member(s).
        Non-authoritative: Indicate the policy will grant a role to a new member.
    """
    AUTHORITATIVE = 'authoritative'
    ROLEAUTHORITATIVE = 'Role-authoritative'
    NONAUTHORITATIVE = 'Non-authoritative'


@dataclass
class GcpIamPolicyCondition:
    """
    Attributes:
        expression: The actual condition written in Common Expression Language (CEL).
        title: A short user description to describe the condition purpose.
        description: (optional) An optional longer description for the condition.
    """
    expression: str
    title: str
    description: Optional[str]


@dataclass
class GcpIamPolicyBinding:
    """
    Attributes:
        members: The list of identities which will be granted the privileges set in the role.
        role: The role which should be applied over the identities.
        condition: (optional) An optional condition to grant the identities with the role privileges only if the condition is met.
    """
    members: List[str]
    role: str
    condition: Optional[GcpIamPolicyCondition]


class IamAccessPolicy(GcpResource):
    """
    A parent class for all IAM policy resources
    Attributes:
        resource_name: The resource name this IAM policy should be attached to.
        bindings: The list of IAM policy attributes.
        policy_type: Relevant for IaC implementation.
    """

    def __init__(self,
                 resource_name: str,
                 bindings: List[GcpIamPolicyBinding],
                 policy_type: GcpIamPolicyType = GcpIamPolicyType.AUTHORITATIVE) -> None:
        super().__init__(GcpResourceType.NONE)
        self.resource_name: str = resource_name
        self.bindings: List[GcpIamPolicyBinding] = bindings
        self.policy_type: GcpIamPolicyType = policy_type

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        pass

    @property
    def is_labeled(self) -> bool:
        pass
