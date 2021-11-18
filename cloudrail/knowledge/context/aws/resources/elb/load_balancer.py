from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.aws.resources.elb.load_balancer_attributes import LoadBalancerAttributes
from cloudrail.knowledge.context.aws.resources.elb.load_balancer_target_group import LoadBalancerTargetGroup
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.utils.tags_utils import filter_tags


class LoadBalancerSchemeType(Enum):
    INTERNAL = 'internal'
    INTERNET_FACING = 'internet-facing'


class LoadBalancerType(Enum):
    NETWORK = 'network'
    APPLICATION = 'application'


@dataclass
class LoadBalancerSubnetMapping:
    allocation_id: str
    private_ipv4_address: str
    subnet_id: str


@dataclass
class LoadBalancerRawData:
    subnets_ids: List[str] = field(default_factory=list)
    security_groups_ids: List[str] = field(default_factory=list)
    subnet_mapping: List[LoadBalancerSubnetMapping] = field(default_factory=list)


class LoadBalancer(NetworkEntity):
    """
        Attributes:
            name: The name of the load balancer.
            scheme_type: The scheme type (internal or internet-facing).
            load_balancer_type: The type of the load balancer (network or application).
            load_balancer_arn: The ARN of the load balancer.
            target_groups: The target groups associated with this LB.
            listener_ports: The ports the listeners associated with this LB are configured to.
    """

    def __init__(self, account: str, region: str, name: str, scheme_type: LoadBalancerSchemeType,
                 load_balancer_type: LoadBalancerType, load_balancer_arn: str):
        super().__init__(name, account, region, AwsServiceName.AWS_LOAD_BALANCER)
        self.scheme_type: LoadBalancerSchemeType = scheme_type
        self.load_balancer_type: LoadBalancerType = load_balancer_type
        self.load_balancer_arn: str = load_balancer_arn
        self.target_groups: List[LoadBalancerTargetGroup] = []
        self.listener_ports: List[int] = []
        self.with_aliases(self.load_balancer_arn)
        self.raw_data = LoadBalancerRawData()
        self.load_balancer_attributes: Optional[LoadBalancerAttributes] = None

    def get_keys(self) -> List[str]:
        return [self.load_balancer_arn]

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.get_arn()

    def get_arn(self) -> str:
        return self.load_balancer_arn

    def get_extra_data(self) -> str:
        load_balancer_type = 'type: {}'.format(self.load_balancer_type) if self.load_balancer_type else ''
        subnet_ids = 'subnet_ids: {}'.format(self.network_resource.subnet_ids) if self.network_resource.subnet_ids else ''
        security_group_ids = 'security_group_ids: {}'.format(self.network_resource.security_groups_ids)
        return ', '.join([load_balancer_type, subnet_ids, security_group_ids])

    def with_raw_data(self, subnets_ids: List[str] = None, security_groups_ids: List[str] = None, subnet_mapping: List[dict] = None) -> LoadBalancer:
        subnet_mapping = subnet_mapping or []
        self.raw_data = LoadBalancerRawData(subnets_ids or [], security_groups_ids or [],
                                            [LoadBalancerSubnetMapping(x.get('allocation_id') or x.get('AllocationId'),
                                                                       x.get('private_ipv4_address') or x.get('IpAddress'),
                                                                       x.get('subnet_id') or x.get('SubnetId')) for x in subnet_mapping])
        return self

    def get_cloud_resource_url(self) -> str:
        return '{0}ec2/v2/home?region={1}#LoadBalancers' \
            .format(self.AWS_CONSOLE_URL, self.region)

    @property
    def is_tagable(self) -> bool:
        return True

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags),
                'scheme_type': self.scheme_type.value,
                'load_balancer_type': self.load_balancer_type.value,
                'listener_ports': self.listener_ports}
