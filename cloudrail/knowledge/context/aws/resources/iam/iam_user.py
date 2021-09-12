from typing import Dict, List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.utils import flat_list
from cloudrail.knowledge.context.aws.resources.iam.iam_group import IamGroup
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.iam.policy import Policy


class IamUser(IamIdentity):
    """
        Attributes:
            name: The name of the user.
            user_id: The ID of the user.
            groups: The groups the user belongs to.
            groups_attach_origin_map: A cache map used to "remember" the origin
                of user-to-group attachments (whether from live account, IaC, etc.).
    """
    def __init__(self, account: str, name: str, user_id: str, qualified_arn: str,
                 permission_boundary_arn: Optional[str], arn: str = None):
        super().__init__(account, qualified_arn, arn, AwsServiceName.AWS_IAM_USER)
        self.name: str = name
        self.user_id: str = user_id
        self.permission_boundary_arn: Optional[str] = permission_boundary_arn
        self.groups: List[IamGroup] = []
        self.groups_attach_origin_map: List[Dict] = []

    def get_policies(self) -> List[Policy]:
        return self.permissions_policies + flat_list([group.permissions_policies for group in self.groups])

    def get_policies_attach_origin_maps(self) -> List[Dict]:
        return self.policy_attach_origin_map + flat_list([group.policy_attach_origin_map for group in self.groups])

    def get_keys(self) -> List[str]:
        return [self.user_id]

    def get_arn(self) -> str:
        return self.qualified_arn

    def __hash__(self):
        return hash(id(self))

    def get_extra_data(self) -> str:
        groups = 'groups: {}'.format(self.groups) if self.groups else ''

        return ', '.join([groups])

    def __str__(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM user'
        else:
            return 'IAM users'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/users/{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.name)

    def clone(self):
        return IamUser(account=self.account, name=self.name, user_id=self.user_id, qualified_arn=self.qualified_arn,
                       permission_boundary_arn=self.permission_boundary_arn, arn=self.arn)

    @property
    def is_tagable(self) -> bool:
        return True
