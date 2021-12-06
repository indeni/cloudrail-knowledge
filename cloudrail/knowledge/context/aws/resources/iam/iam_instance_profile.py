from typing import List

from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.utils.tags_utils import filter_tags


class IamInstanceProfile(AwsResource):
    """
        Attributes:
            role_name: The name of the role.
            iam_instance_profile_name: The name of the instance profile.
            ec2_instance_data: The Ec2Instance using this profile.
    """

    def __init__(self, account: str, region: str, role_name: str, iam_instance_profile_name: str):
        super().__init__(account, region, AwsServiceName.AWS_IAM_INSTANCE_PROFILE)
        self.role_name: str = role_name
        self.region: str = region
        self.iam_instance_profile_name: str = iam_instance_profile_name
        self.ec2_instance_data: Ec2Instance = None
        self.with_aliases(self.iam_instance_profile_name)

    def get_keys(self) -> List[str]:
        return [self.iam_instance_profile_name]

    def get_extra_data(self) -> str:
        role_name = 'role_name: {}'.format(self.role_name) if self.role_name else ''

        return ', '.join([role_name])

    def get_id(self) -> str:
        return self.iam_instance_profile_name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'IAM Instance profile'
        else:
            return 'IAM Instance profiles'

    def get_arn(self) -> str:
        return f'arn:aws:iam::{self.account}:instance-profile/{self.iam_instance_profile_name}'

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home#/roles/{1}'\
            .format(self.AWS_CONSOLE_URL, self.role_name)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'role_name': self.role_name,
                'iam_instance_profile_name': self.iam_instance_profile_name}
