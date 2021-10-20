from typing import List, Optional, Union

from cloudrail.knowledge.context.aws.resources.ec2.elastic_ip import ElasticIp
from cloudrail.knowledge.context.aws.resources.elb.load_balancer import LoadBalancer
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource


class GlobalAcceleratorEndpointGroup(AwsResource):
    """
        Attributes:
            account: The account ID in which this resource operates.
            region: The region in which this resource operates.
            listener_arn: The Load Balancer Listener which this endpoint associated with.
            endpoint_arn: The ARN of the Global Accelerator Endpoint.
            endpoint_config_id: The ID of the endpoint object.
            client_ip_preservation_enabled: Is client IP address preservation is enabled for an Application Load Balancer endpoint.
    """

    def __init__(self,
                 account: str,
                 listener_arn: str,
                 endpoint_arn: str,
                 endpoint_config_id: str,
                 client_ip_preservation_enabled: bool,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_GLOBALACCELERATOR_ENDPOINT_GROUP)
        self.listener_arn: str = listener_arn
        self.endpoint_arn: str = endpoint_arn
        self.endpoint_config_id: str = endpoint_config_id
        self.client_ip_preservation_enabled: bool = client_ip_preservation_enabled
        self.region: str = region
        self.endpoint_resource: Optional[Union[LoadBalancer, ElasticIp]] = None

    def get_keys(self) -> List[str]:
        return [self.endpoint_arn]

    def get_arn(self) -> str:
        return self.endpoint_arn

    def get_cloud_resource_url(self) -> str:
        return f'https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#EndpointGroupDetails:EndpointGroupArn={self.endpoint_arn}'

    @property
    def is_tagable(self) -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'listener_arn': self.listener_arn,
                'endpoint_arn': self.endpoint_arn,
                'endpoint_config_id': self.endpoint_config_id,
                'client_ip_preservation_enabled': self.client_ip_preservation_enabled}
