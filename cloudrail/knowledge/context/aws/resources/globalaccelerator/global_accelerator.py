from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.globalaccelerator.global_accelerator_attributes import GlobalAcceleratorAttribute
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class GlobalAccelerator(AwsResource):
    """
        Attributes:
            account: The account ID in which this resource operates.
            region: The region in which this resource operates.
            accelerator_name: The Global Accelerator name.
            arn: The ARN of the Global Accelerator.
    """

    def __init__(self,
                 account: str,
                 accelerator_name: str,
                 arn: str):
        super().__init__(account, 'us-west-2', AwsServiceName.AWS_GLOBALACCELERATOR_ACCELERATOR)
        self.accelerator_name: str = accelerator_name
        self.arn: str = arn
        self.region: str = 'us-west-2'
        self.attributes: Optional[GlobalAcceleratorAttribute] = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.accelerator_name

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        return f'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#AcceleratorDetails:AcceleratorArn={self.arn}'

    @property
    def is_tagable(self) -> bool:
        return True
