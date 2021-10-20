from typing import List

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class RoleLastUsed(AwsResource):
    """
        Attributes:
            role_name: The name of the role.
            arn: The ARN of the role.
            last_used_date: The last date the role was used in.
    """

    def __init__(self, account: str,
                 region: str,
                 role_name: str,
                 arn: str,
                 last_used_date: str):
        super().__init__(account, region, AwsServiceName.AWS_IAM_ROLE)
        self.role_name: str = role_name
        self.arn: str = arn
        self.last_used_date: str = last_used_date

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Role Last Used'
        else:
            return 'Roles Last Used'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/roles/{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.role_name)

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'role_name': self.role_name,
                'last_used_date': self.last_used_date}
