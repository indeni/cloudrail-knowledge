from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict

from cloudrail.knowledge.context.aws.resources.ec2.internet_gateway import InternetGateway
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpoint


@dataclass
class VpcRawData:
    main_route_table_id: Optional[str] = None
    default_route_table_id: Optional[str] = None
    default_security_group_id: Optional[str] = None


class VpcAttribute(AwsResource):

    def __init__(self, account: str, region: str, vpc_id: str, attribute_name: str, enable: bool):
        super().__init__(account, region, AwsServiceName.NONE)
        self.vpc_id: str = vpc_id
        self.attribute_name: str = attribute_name
        self.enable: bool = enable

    def get_keys(self) -> List[str]:
        return [self.vpc_id, self.attribute_name]

    def get_cloud_resource_url(self) -> Optional[str]:
        if self.attribute_name == 'EnableDnsSupport':
            return '{0}vpc/home?region={1}#EditDnsResolution:VpcId={2}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.vpc_id)
        else:
            return '{0}vpc/home?region={1}#EditDnsHostnames:VpcId={2}' \
                .format(self.AWS_CONSOLE_URL, self.region, self.vpc_id)

    def get_friendly_name(self) -> str:
        return f'{self.vpc_id} dns attribute={self.attribute_name} is enable={self.enable}'

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False


class Vpc(AwsResource):

    def __init__(self,
                 vpc_id: str,
                 cidr_block: List[str],
                 ipv6_cidr_block: Optional[List[str]],
                 name: str,
                 account: str,
                 region: str,
                 friendly_name: str = None,
                 is_default: bool = False,
                 enable_dns_support: bool = None,
                 enable_dns_hostnames: bool = None):
        super().__init__(account, region, AwsServiceName.AWS_VPC)
        self.vpc_id: str = vpc_id
        self.with_aliases(vpc_id)
        self.cidr_block: List[str] = cidr_block
        self.ipv6_cidr_block: Optional[List[str]] = ipv6_cidr_block
        self.name: str = name
        self.friendly_name: Optional[str] = friendly_name
        self.is_default: Optional[bool] = is_default
        self.enable_dns_support: Optional[bool] = enable_dns_support
        self.enable_dns_hostnames: Optional[bool] = enable_dns_hostnames

        self.main_route_table: Optional[RouteTable] = None
        self.endpoints: List[VpcEndpoint] = []
        self.default_security_group: Optional[SecurityGroup] = None
        self.default_nacl: Optional[NetworkAcl] = None
        self.subnets_by_az_map: Dict[str, List[Subnet]] = {}
        self.internet_gateway: Optional[InternetGateway] = None
        self.raw_data: VpcRawData = VpcRawData()

    def get_keys(self) -> List[str]:
        return [self.vpc_id]

    def get_id(self) -> str:
        return self.vpc_id

    def get_name(self) -> str:
        return self.name

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#VpcDetails:VpcId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.vpc_id)

    def get_extra_data(self) -> str:
        cidr_block = 'cidr_block: {}'.format(self.cidr_block) if self.cidr_block else ''
        main_route_table_id = 'main_route_table_id: {}'.format(
            self.raw_data.main_route_table_id) if self.raw_data.main_route_table_id else 'No route table ID provided, using default'
        is_default = 'is_default: {}'.format(self.is_default) if self.is_default else 'is_default is unknown'

        return ', '.join([cidr_block, main_route_table_id, is_default])

    def with_raw_data(self, main_route_table_id: str, default_route_table_id: str, default_security_group_id: str) -> Vpc:
        self.raw_data = VpcRawData(main_route_table_id, default_route_table_id, default_security_group_id)
        return self

    def __str__(self) -> str:
        return self.name or self.vpc_id

    @property
    def subnets(self) -> List['Subnet']:
        return [subnet for subnet_list in self.subnets_by_az_map.values() for subnet in subnet_list]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'VPC'
        else:
            return "VPC's"

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
