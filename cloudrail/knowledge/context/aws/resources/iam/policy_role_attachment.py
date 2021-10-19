from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class PolicyRoleAttachment(AwsResource):
    """
        Attributes:
            policy_arn: The policy to attach to the role.
            role_name: The name of the role to attach the policy to.
    """

    def __init__(self, account: str, policy_arn: str, role_name: str):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_ROLE_POLICY_ATTACHMENT)
        self.policy_arn: str = policy_arn
        self.role_name: str = role_name

    def get_keys(self) -> List[str]:
        return [self.policy_arn, self.role_name]

    def get_extra_data(self) -> str:
        policy_arn = 'policy_arn: {}'.format(self.policy_arn) if self.policy_arn else ''
        role_name = 'role_name: {}'.format(self.role_name) if self.role_name else ''

        return ', '.join([policy_arn, role_name])

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/roles/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.role_name)

    def get_arn(self) -> str:
        return self.policy_arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'policy_arn': self.policy_arn,
                'role_name': self.role_name}
