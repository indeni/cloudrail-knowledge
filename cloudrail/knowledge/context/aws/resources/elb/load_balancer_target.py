from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class LoadBalancerTarget(AwsResource):
    """
        Attributes:
            target_group_arn: The ARN of the target group this target belongs to.
            target_id: The ID of this target.
            port: The port this target listens on.
            target_instance: Set to an Ec2Instance of applicable.
    """

    def __init__(self, target_group_arn: str, target_id: str, port: int, account: str, region: str):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP_ATTACHMENT)
        self.target_group_arn: str = target_group_arn
        self.target_id: str = target_id
        self.port: int = port
        self.target_instance = None

    def get_keys(self) -> List[str]:
        return [self.target_group_arn, self.target_id]

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ec2/v2/home?region={1}#TargetGroup:targetGroupArn={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.target_group_arn)

    def get_arn(self) -> str:
        return self.target_group_arn

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'target_group_arn': self.target_group_arn,
                'target_id': self.target_id,
                'port': self.port}
