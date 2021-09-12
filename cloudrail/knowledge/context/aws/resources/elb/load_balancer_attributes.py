from dataclasses import dataclass
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


@dataclass
class LoadBalancerAccessLogs:
    """
        Attributes:
            bucket: The S3 bucket to store logs into.
            prefix: The S3 bucket prefix (optional).
            enable: Indication if access logs are enabled.

    """
    bucket: str
    prefix: str
    enabled: bool


class LoadBalancerAttributes(AwsResource):
    """
        Attributes:
            load_balancer_arn: The ARN of the load balancer.
            drop_invalid_header_fields: An indication if the application load balancer remove invalid http headers or send to the targets as is.
            access_logs: Block of settings for this load balancer access logs.
    """
    def __init__(self,
                 account: str,
                 region: str,
                 load_balancer_arn: str,
                 drop_invalid_header_fields: bool,
                 access_logs: Optional[LoadBalancerAccessLogs]):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER)
        self.load_balancer_arn: str = load_balancer_arn
        self.drop_invalid_header_fields: Optional[bool] = drop_invalid_header_fields
        self.access_logs: Optional[LoadBalancerAccessLogs] = access_logs

    def get_keys(self) -> List[str]:
        return [self.load_balancer_arn, 'attributes']

    def get_arn(self) -> str:
        pass

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#LoadBalancers' \
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return False
