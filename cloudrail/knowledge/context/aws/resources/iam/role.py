from typing import List, Dict, Optional

from cloudrail.knowledge.context.connection import PolicyEvaluation
from cloudrail.knowledge.context.aws.resources.iam.policy import AssumeRolePolicy
from cloudrail.knowledge.context.aws.resources.iam.role_last_used import RoleLastUsed
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.utils.tags_utils import filter_tags


class Role(IamIdentity):
    """
        Attributes:
            role_name: THe name of the role.
            role_id: The role's ID.
            permission_boundary_arn: The ARN of the permission boundary if one
                applies (may be None).
            creation_date: The date of creation of the role.
            arn: The ARN of the role.
            assume_role_policy: The assume role policy.
            policy_evaluation_result_map: A caching of the policy evaluation
                for the role.
            last_used_date: Last date the role was used (comes from an API call
                made to the AWS IAM API).
    """

    def __init__(self, account: str,
                 qualified_arn: str,
                 role_name: str,
                 role_id: str,
                 permission_boundary_arn: Optional[str],
                 creation_date: str,
                 arn: str = None):
        super().__init__(account, qualified_arn, arn, AwsServiceName.AWS_IAM_ROLE)
        self.role_name: str = role_name
        self.role_id: str = role_id
        self.permission_boundary_arn: Optional[str] = permission_boundary_arn
        self.assume_role_policy: AssumeRolePolicy = None
        self.policy_evaluation_result_map: Dict[str, PolicyEvaluation] = {}
        self.creation_date: str = creation_date
        self.last_used_date: RoleLastUsed = None
        self.with_aliases(role_name, role_id, self.qualified_arn)

    def get_keys(self) -> List[str]:
        return [self.qualified_arn]

    def get_id(self) -> str:
        return self.role_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Role'
        else:
            return 'IAM Roles'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/roles/{2}' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.role_name)

    @property
    def is_ever_used(self) -> bool:
        return bool(self.last_used_date and self.last_used_date.last_used_date)

    def clone(self):
        role = Role(account=self.account, qualified_arn=self.qualified_arn, role_name=self.role_name, role_id=self.role_id,
                    permission_boundary_arn=self.permission_boundary_arn, arn=self.arn, creation_date=self.creation_date)
        role.assume_role_policy = self.assume_role_policy
        return role

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'role_name': self.role_name,
                'permission_boundary_arn': self.permission_boundary_arn}
