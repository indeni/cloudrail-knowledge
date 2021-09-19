from typing import List
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.cloudwatch.cloudwatch_logs_destination_policy import CloudWatchLogsDestinationPolicy
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class CloudWatchLogsDestination(AwsResource):
    """
        Attributes:
            name: The name of the destination.
            arn: THe ARN of the destination.
            policy: The destination's policy, if configured (may be None).
    """
    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 arn: str):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDWATCH_LOG_DESTINATION)
        self.name: str = name
        self.arn: str = arn
        self.policy: CloudWatchLogsDestinationPolicy = None

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudWatch Logs Destination'
        else:
            return 'CloudWatch Logs Destinations'

    def get_arn(self) -> str:
        return self.arn

    def get_cloud_resource_url(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
