from typing import List
from cloudrail.knowledge.context.aws.resources.iam.iam_identity import IamIdentity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class IamGroup(IamIdentity):
    """
        Attributes:
            name: The name of the IAM Group.
            group_id: The ID of the group.
    """

    def __init__(self, account: str, name: str, group_id: str, qualified_arn: str, arn: str = None):
        super().__init__(account, qualified_arn, arn, AwsServiceName.AWS_IAM_GROUP)
        self.name: str = name
        self.group_id: str = group_id

    def get_keys(self) -> List[str]:
        return [self.group_id]

    def get_name(self) -> str:
        return self.name

    def get_extra_data(self) -> str:
        policies = 'policies: {}'.format(self.permissions_policies) if self.permissions_policies else ''

        return ', '.join([policies])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Group'
        else:
            return 'IAM Groups'

    def clone(self):
        return IamGroup(account=self.account, name=self.name, group_id=self.group_id, qualified_arn=self.qualified_arn, arn=self.arn)

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/groups/{2}' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.name)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name}
