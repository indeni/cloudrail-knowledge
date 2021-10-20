from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class IamUserGroupMembership(AwsResource):
    """
        Attributes:
            user: The user the membership is focused on.
            groups: The groups the user should be a member of.
    """

    def __init__(self, account: str, user: str, groups: List[str]):
        super().__init__(account=account, region=self.GLOBAL_REGION,
                         tf_resource_type=AwsServiceName.AWS_IAM_USER_GROUP_MEMBERSHIP)
        self.user: str = user
        self.groups: List[str] = groups

    def get_keys(self) -> List[str]:
        return [self.user] + self.groups

    def get_extra_data(self) -> str:
        user = 'user: {}'.format(self.user) if self.user else ''
        groups = 'groups: {}'.format(self.groups) if self.groups else ''

        return ', '.join([user, groups])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM user group membership'
        else:
            return 'IAM user group memberships'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/users/{2}' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.user)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'user': self.user,
                'groups': self.groups}
