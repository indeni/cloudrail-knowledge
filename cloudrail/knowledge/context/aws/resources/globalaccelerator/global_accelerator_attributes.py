from typing import List, Optional
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class GlobalAcceleratorAttribute(AwsResource):
    """
        Attributes:
            flow_logs_enabled: Indicating if the flow logs are enabled for the Global Accelerator.
            flow_logs_s3_bucket: The S3 bucket to store the logs, if enabled.
            flow_logs_s3_prefix: The prefix name for the logs files, if enabled.
            arn: The ARN of the Global Accelerator.
    """

    def __init__(self,
                 account: str,
                 flow_logs_enabled: bool,
                 flow_logs_s3_bucket: Optional[str],
                 flow_logs_s3_prefix: Optional[str],
                 accelerator_arn: str):
        super().__init__(account, 'us-west-2', AwsServiceName.AWS_GLOBALACCELERATOR_ACCELERATOR)
        self.flow_logs_enabled: bool = flow_logs_enabled
        self.flow_logs_s3_bucket: Optional[str] = flow_logs_s3_bucket
        self.flow_logs_s3_prefix: Optional[str] = flow_logs_s3_prefix
        self.accelerator_arn: str = accelerator_arn
        self.region: str = 'us-west-2'

    def get_keys(self) -> List[str]:
        return [self.accelerator_arn]

    def get_name(self) -> str:
        return f'Attributes for Global Accelerator with ARN {self.accelerator_arn}'

    def get_arn(self) -> str:
        return self.accelerator_arn

    def get_cloud_resource_url(self) -> str:
        return f'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#AcceleratorDetails:AcceleratorArn={self.accelerator_arn}'

    @property
    def is_tagable(self) -> bool:
        return False
