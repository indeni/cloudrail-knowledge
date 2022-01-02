from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target import LoadBalancerTarget
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.tags_utils import filter_tags


class LoadBalancerTargetGroup(AwsResource):
    """
        Attributes:
            port: The port the target group listens on.
            protocol: The protocol the target group listens to.
            vpc_id: The VPC the target group is in.
            target_group_arn: The ARN of the target group.
            target_group_name: The name of the target group.
            target_type: The type of the target, types vary based on the type
                of the load balancer itself.
            targets: The targets within this group.
    """

    def __init__(self,
                 port: int,
                 protocol: IpProtocol,
                 vpc_id: str,
                 target_group_arn: str,
                 target_group_name: str,
                 target_type: str,
                 account: str,
                 region: str):
        super().__init__(account, region, AwsServiceName.AWS_LOAD_BALANCER_TARGET_GROUP)
        self.port: int = port
        self.protocol: IpProtocol = protocol
        self.vpc_id: str = vpc_id
        self.target_group_arn: str = target_group_arn
        self.target_group_name: str = target_group_name
        self.target_type: str = target_type
        self.targets: List[LoadBalancerTarget] = []
        self.with_aliases(target_group_arn)

    def get_keys(self) -> List[str]:
        return [self.target_group_arn]

    def get_arn(self) -> str:
        return self.target_group_arn

    def get_name(self) -> str:
        return self.target_group_name

    def get_id(self) -> str:
        return self.target_group_arn

    def get_extra_data(self) -> str:
        target_type = 'type: {}'.format(self.target_type) if self.target_type else ''
        vpc_id = 'vpc_id: {}'.format(self.vpc_id) if self.vpc_id else ''
        protocol = 'protocol: {}'.format(self.protocol) if self.protocol else ''
        port = 'port: {}'.format(self.port) if self.port else ''
        return ', '.join([target_type, vpc_id, protocol, port])

    def get_cloud_resource_url(self) -> Optional[str]:
        return '{0}ec2/v2/home?region={1}#TargetGroup:targetGroupArn={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.target_group_arn)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'port': self.port,
                'protocol': self.protocol.__repr__(),
                'vpc_id': self.vpc_id,
                'target_group_arn': self.target_group_arn,
                'target_type': self.target_type}
