from abc import abstractmethod
from typing import Iterable, List, Dict, Optional, Set, Union

from cloudrail.knowledge.context.aws.aws_connection import ConnectionInstance
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.iam.policy import InlinePolicy, ManagedPolicy, Policy, PolicyType
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.cloneable import Cloneable


class IamIdentity(AwsResource, ConnectionInstance, Cloneable):
    """
        Attributes:
            qualified_arn: A Cloudrail-caculated ARN for the role that ensures
                it's the same whether the role came from infrastructure-as-code
                (such as Terraform) or the live AWS environment.
            arn: The ARN of the IAM identity.
            permissions_policies: One or more policies used to give the IAM entity
                permissions to take certain actions.
            permission_boundary: The permission boundary limiting the IAM entity's
                permissions.
    """
    def __init__(self, account: str, qualified_arn: str, arn: str, tf_resource_type: AwsServiceName):
        AwsResource.__init__(self, account=account, region=self.GLOBAL_REGION, tf_resource_type=tf_resource_type)
        ConnectionInstance.__init__(self)
        self.qualified_arn: str = qualified_arn
        self.arn: str = arn
        self.permissions_policies: List[Union[ManagedPolicy, InlinePolicy]] = []
        self.permission_boundary: Optional[Policy] = None
        self.policy_to_escalation_actions_map: Dict[str, Set[str]] = dict()
        self.policy_attach_origin_map: List[Dict] = []

    @abstractmethod
    def get_keys(self) -> List[str]:
        pass

    @abstractmethod
    def clone(self):
        pass

    def get_policies_attach_origin_maps(self) -> List[Dict]:
        return self.policy_attach_origin_map

    def get_policies(self) -> List[Policy]:
        return self.permissions_policies

    def get_arn(self) -> str:
        return self.qualified_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Identity'
        else:
            return 'IAM Identities'

    def deep_copy(self):
        iam_entity = self.clone()
        iam_entity.inbound_connections = set(self.inbound_connections)
        iam_entity.inbound_connections = set(self.outbound_connections)
        iam_entity.qualified_arn = self.qualified_arn
        iam_entity.arn = self.arn
        iam_entity.permissions_policies = [policy.clone() for policy in self.permissions_policies]
        for permissions_policy in iam_entity.permissions_policies:
            permissions_policy.policy_type = PolicyType.IDENTITY_POLICY
        iam_entity.permission_boundary = self.permission_boundary.clone() if self.permission_boundary else None
        iam_entity.policy_to_escalation_actions_map = dict(self.policy_to_escalation_actions_map)
        return iam_entity

    @property
    def is_tagable(self) -> bool:
        return False

    def attach_policy_origin_data(self, policies: Iterable[ManagedPolicy], policy_attachments_list: List[AwsResource]):
        for policy in policies:
            policy_attach = next((policy_attach for policy_attach in policy_attachments_list if policy.get_arn() == policy_attach.get_arn()), None)
            if policy_attach:
                self.policy_attach_origin_map.append({policy.get_name(): policy_attach.origin})
            if policy not in self.permissions_policies:
                self.permissions_policies.append(policy)
