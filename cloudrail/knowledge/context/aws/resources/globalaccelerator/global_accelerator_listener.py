from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class GlobalAcceleratorListener(AwsResource):
    """
        Attributes:
            account: The account ID in which this resource operates.
            region: The region in which this resource operates.
            listener_arn: The Load Balancer Listener resource ARN.
            accelerator_arn: The ARN of the Global Accelerator resource.
    """

    def __init__(self,
                 account: str,
                 listener_arn: str,
                 accelerator_arn: str):
        super().__init__(account, 'us-west-2', AwsServiceName.AWS_GLOBALACCELERATOR_LISTENER)
        self.listener_arn: str = listener_arn
        self.accelerator_arn: str = accelerator_arn
        self.region: str = 'us-west-2'

    def get_keys(self) -> List[str]:
        return [self.listener_arn]

    def get_arn(self) -> str:
        return self.listener_arn

    def get_cloud_resource_url(self) -> str:
        return f'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#ListenerDetails:ListenerArn={self.listener_arn}'

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'listener_arn': self.listener_arn,
                'accelerator_arn': self.accelerator_arn}
