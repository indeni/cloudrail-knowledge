from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class IamUsersLoginProfile(AwsResource):
    """
        Attributes:
            name: The name of the user the login profile is for.
    """

    def __init__(self,
                 name: str,
                 account: str):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_USER_LOGIN_PROFILE)
        self.name: str = name

    def get_keys(self) -> List[str]:
        return [self.name]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM user login profile'
        else:
            return 'IAM user login profiles'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/users/{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.name)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name}
