import json
import uuid
from enum import Enum
from typing import List, Dict

from cloudrail.knowledge.context.cloneable import Cloneable
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect


class PolicyType(str, Enum):
    IDENTITY_POLICY = 'IDENTITY_POLICY'
    RESOURCE_POLICY = 'RESOURCE_POLICY'
    SERVICE_CONTROL_POLICY = 'SERVICE_CONTROL_POLICY'


class Policy(AwsResource, Cloneable):
    """
        Attributes:
            statements: The list of statements in the policy.
            uuid: A randomly generated uuid for the policy (ignore, for internal use).
            raw_document: The raw JSON of the policy.
            access_analyzer_findings: The results from running IAM Access Analyzer's
                policy validation API on this policy's JSON.
            policy_type: The type of the policy (identity, resource, SCP).
    """
    def __init__(self,
                 account: str,
                 statements: List[PolicyStatement],
                 raw_document: str = None,
                 aws_service_name: AwsServiceName = AwsServiceName.AWS_IAM_POLICY,
                 policy_type: PolicyType = PolicyType.RESOURCE_POLICY):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=aws_service_name)
        self.statements: List[PolicyStatement] = statements
        self._init_statements()
        self.uuid: str = str(uuid.uuid4())
        self.raw_document = raw_document
        if isinstance(self.raw_document, dict):
            self.raw_document = json.dumps(self.raw_document)
        self.access_analyzer_findings = []
        self.policy_type = policy_type

    def _init_statements(self):
        for statement in self.statements:
            statement.policy = self

    def add_statement(self, statement: PolicyStatement) -> None:
        statement.policy = self
        self.statements.append(statement)

    def add_all_statements(self, statements: List[PolicyStatement]) -> None:
        return self.statements.extend(statements)

    def reset_statements(self) -> None:
        self.statements = []

    def get_keys(self) -> List[str]:
        raise NotImplementedError('Policy.get_keys() invoked when it shouldnt')

    def get_statements_by_effect(self) -> Dict[StatementEffect, List[PolicyStatement]]:
        statements_by_effect_map: Dict[StatementEffect, List[PolicyStatement]] = {StatementEffect.ALLOW: [], StatementEffect.DENY: []}
        for statement in self.statements:
            statement_copy: PolicyStatement = statement.clone()
            statements_by_effect_map[statement_copy.effect].append(statement_copy)
        return statements_by_effect_map

    def get_cloud_resource_url(self) -> str:
        pass

    def get_arn(self) -> str:
        pass

    def clone(self):
        policy = Policy(account=self.account,
                        statements=[stat.clone() for stat in self.statements],
                        raw_document=self.raw_document)
        policy.tf_resource_type = self.tf_resource_type
        policy.with_aliases(*self._aliases)
        policy.iac_state = self.iac_state
        policy.is_pseudo = self.is_pseudo
        policy.aws_service_attributes = self.aws_service_attributes
        policy.tags = self.tags
        return policy

    @property
    def is_tagable(self) -> bool:
        return False


class ManagedPolicy(Policy):

    def __init__(self, account: str, policy_id: str,
                 policy_name: str, arn: str, statements: List[PolicyStatement], raw_document: str):
        self.account: str = account
        self.policy_id: str = policy_id
        self.policy_name: str = policy_name
        self.arn: str = arn
        super().__init__(account, statements, raw_document, policy_type=PolicyType.IDENTITY_POLICY)

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.policy_name

    def get_arn(self) -> str:
        return self.arn

    def __str__(self) -> str:
        return self.policy_name

    def get_cloud_resource_url(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

class InlinePolicy(Policy):

    def __init__(self, account: str, owner_name: str,
                 policy_name: str, statements: List[PolicyStatement], raw_document: str):
        self.account: str = account
        self.owner_name: str = owner_name
        self.policy_name: str = policy_name
        super().__init__(account, statements, raw_document, policy_type=PolicyType.IDENTITY_POLICY)

    def get_keys(self) -> List[str]:
        return [self.account, self.policy_name, self.owner_name]

    def get_name(self) -> str:
        return self.policy_name

    def __str__(self) -> str:
        return self.policy_name

    def get_cloud_resource_url(self) -> str:
        pass


class AssumeRolePolicy(Policy):
    """
        Attributes:
            role_name: The name of the role that uses this policy.
            role_arn: The ARN of the role that uses this policy.
            is_allowing_external_assume: An indication on if this policy can be assumed by a resource outside of this policy's account.
    """
    def __init__(self, account: str, role_name: str,
                 role_arn: str, statements: List[PolicyStatement], raw_document: str):
        self.role_name: str = role_name
        self.role_arn: str = role_arn
        self.is_allowing_external_assume: bool = None
        super().__init__(account, statements, raw_document)

    def get_keys(self) -> List[str]:
        return [self.role_arn]

    def get_name(self) -> str:
        return self.role_name + ' assume role policy'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/roles/{2}?section=trust' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.role_name)
