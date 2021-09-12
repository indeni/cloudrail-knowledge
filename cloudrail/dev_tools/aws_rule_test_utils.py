from typing import Optional, TypeVar, Type

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.route_table import RouteTable
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.networking_config.network_entity import NetworkEntity


_T = TypeVar('_T', bound=NetworkEntity)


def create_empty_network_entity(_type: Type[_T], subnet: Optional[Subnet] = None) -> _T:
    instance: NetworkEntity = create_empty_entity(_type)
    if not subnet:
        subnet = create_empty_entity(Subnet)
        subnet.name = 'subnet-name'
    if not subnet.vpc:
        vpc = create_empty_entity(Vpc)
        subnet.vpc = vpc
    if not subnet.network_acl:
        nacl = create_empty_entity(NetworkAcl)
        nacl.name = 'network-acl-name'
        subnet.network_acl = nacl
    if not subnet.route_table:
        subnet.route_table = create_empty_entity(RouteTable)
        subnet.route_table.name = 'route-table-name'
    eni = create_empty_entity(NetworkInterface)
    eni.owner = instance
    eni.subnet = subnet
    instance.network_resource.add_interface(eni)
    return instance
