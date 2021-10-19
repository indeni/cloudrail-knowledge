from typing import List

from cloudrail.knowledge.context.aws.resources.aws_policied_resource import PoliciedResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class CloudWatchLogsDestination(PoliciedResource):
    """
        Attributes:
            name: The name of the destination.
            arn: THe ARN of the destination.
    """

    def __init__(self,
                 account: str,
                 region: str,
                 name: str,
                 arn: str):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDWATCH_LOG_DESTINATION)
        self.name: str = name
        self.arn: str = arn

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

    def to_drift_detection_object(self) -> dict:
        return {'name': self.name}
