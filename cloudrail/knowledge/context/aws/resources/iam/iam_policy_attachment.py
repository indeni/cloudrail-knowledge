from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class IamPolicyAttachment(AwsResource):
    """
        Attributes:
            policy_arn: The ARN of the policy to attach.
            users: The list of users to attach the policy to, may be empty
                or None.
            roles: The list of roles to attach the policy to, may be empty
                or None.
            groups: The list of groups to attach the policy to, may be empty
                or None.

    """

    def __init__(self, account: str,
                 policy_arn: str,
                 attachment_name: str,
                 users: Optional[List],
                 roles: Optional[List],
                 groups: Optional[List]):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_POLICY_ATTACHMENT)
        self.policy_arn: str = policy_arn
        self.attachment_name: str = attachment_name
        self.users: Optional[List] = users
        self.roles: Optional[List] = roles
        self.groups: Optional[List] = groups

    def get_keys(self) -> List[str]:
        return [self.attachment_name]

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/policies'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1')

    def get_arn(self) -> str:
        return self.policy_arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'policy_arn': self.policy_arn,
                'attachment_name': self.attachment_name,
                'users': self.users,
                'roles': self.roles,
                'groups': self.groups}
