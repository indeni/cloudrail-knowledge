from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class PolicyUserAttachment(AwsResource):
    """
        Attributes:
            policy_arn: The policy to attach to the user.
            user_id: The ID of the user to attach the policy to.
            user_name: The name of the user to attach the policy to.
    """

    def __init__(self, account: str, policy_arn: str, user_id: str, user_name: str):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_USER_POLICY_ATTACHMENT)
        self.policy_arn: str = policy_arn
        self.user_id: str = user_id
        self.user_name: str = user_name

    def get_keys(self) -> List[str]:
        return [self.policy_arn, self.user_id]

    def get_extra_data(self) -> str:
        policy_arn = 'policy_arn: {}'.format(self.policy_arn) if self.policy_arn else ''
        user_id = 'user_id: {}'.format(self.user_id) if self.user_id else ''

        return ', '.join([policy_arn, user_id])

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/users/{2}' \
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.user_name)

    def get_arn(self) -> str:
        return self.policy_arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'policy_arn': self.policy_arn,
                'user_id': self.user_id,
                'user_name': self.user_name}
