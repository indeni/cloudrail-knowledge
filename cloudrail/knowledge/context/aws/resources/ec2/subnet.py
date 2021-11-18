from typing import List

from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.utils.tags_utils import filter_tags


class Subnet(AwsResource):
    """
        Attributes:
            subnet_id: The ID of the subnet.
            vpc_id: The ID of the VPC the subnet belongs to.
            vpc: The VPC the subnet bleongs to.
            cidr_block: The subnet's CIDR block.
            name: The name of the subnet.
            availability_zone: The AZ the subnet is in.
            map_public_ip_on_launch: True if resources should have a public IP
                assigned to them upon launch.
            is_default: True if it's the default subnet of a VPC in an AZ.
            route_table: The main route table associated with this subnet.
            network_acl: The main NACL associated with this subnet.
    """

    def __init__(self,
                 subnet_id: str,
                 vpc_id: str,
                 cidr_block: str,
                 name: str,
                 availability_zone: str,
                 map_public_ip_on_launch: bool,
                 region: str,
                 account: str,
                 is_default: bool = False):
        super().__init__(account, region, AwsServiceName.AWS_SUBNET)
        self.subnet_id: str = subnet_id
        self.map_public_ip_on_launch = map_public_ip_on_launch
        self.vpc_id: str = vpc_id
        self.cidr_block: str = cidr_block
        self.name: str = name
        self.availability_zone: str = availability_zone
        self.is_default: bool = is_default

        self.route_table: RouteTable = None
        self.network_acl: NetworkAcl = None
        self.vpc: 'Vpc' = None
        self.with_aliases(subnet_id)

    def get_keys(self) -> List[str]:
        return [self.subnet_id]

    def get_id(self) -> str:
        return self.subnet_id

    def get_extra_data(self) -> str:
        vpc = 'vpc: {}'.format(self.vpc.get_friendly_name()) if self.vpc else ''
        network_acl = 'network_acl: {}'.format(self.network_acl.get_friendly_name()) if self.network_acl else ''
        return ', '.join([vpc, network_acl])

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#SubnetDetails:subnetId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.subnet_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True

    def get_name(self) -> str:
        return self.name

    def to_drift_detection_object(self) -> dict:
        return {'tags': filter_tags(self.tags), 'vpc_id': self.vpc_id,
                'cidr_block': self.cidr_block,
                'name': self.name,
                'map_public_ip_on_launch': self.map_public_ip_on_launch,
                'is_default': self.is_default}
