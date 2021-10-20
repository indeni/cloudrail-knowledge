from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class PolicyGroupAttachment(AwsResource):
    """
        Attributes:
            policy_arn: The policy to attach to the group.
            group_id: The ID of the group to attach the policy to.
            group_name: The name of the group to attach the policy to.
    """

    def __init__(self, account: str, policy_arn: str, group_id: str, group_name: str):
        super().__init__(account=account, region=self.GLOBAL_REGION, tf_resource_type=AwsServiceName.AWS_IAM_GROUP_POLICY_ATTACHMENT)
        self.policy_arn: str = policy_arn
        self.group_id: str = group_id
        self.group_name: str = group_name

    def get_keys(self) -> List[str]:
        return [self.account, self.policy_arn, self.group_name]

    def get_cloud_resource_url(self) -> str:
        return '{0}iam/home?region={1}#/groups/{2}'\
            .format(self.AWS_CONSOLE_URL, 'us-east-1', self.group_name)

    def get_arn(self) -> str:
        return self.policy_arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'policy_arn': self.policy_arn,
                'group_id': self.group_id,
                'group_name': self.group_name}
