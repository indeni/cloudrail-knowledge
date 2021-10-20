from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class IamGroupMembership(AwsResource):
    """
        Attributes:
            name: The name of the group membership.
            group: The group the users belong to.
            users: The list of users who are members of the designated group.
    """

    def __init__(self, account: str, name: str, group: str, users: List[str]):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_GROUP_MEMBERSHIP)
        self.name: str = name
        self.group: str = group
        self.users: List[str] = users

    def get_keys(self) -> List[str]:
        return [self.name]

    def get_extra_data(self) -> str:
        group = 'group: {}'.format(self.group) if self.group else ''
        users = 'users: {}'.format(self.users) if self.users else ''

        return ', '.join([group, users])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Group Membership'
        else:
            return 'IAM Group Memberships'

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/groups/{2}' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.group)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name,
                'group': self.group,
                'users': self.users}
