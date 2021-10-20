from __future__ import annotations
from enum import Enum
from typing import List, Tuple

from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.range_util import get_range_numbers_overlap, EMPTY_RANGE
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource

from cloudrail.knowledge.utils.utils import get_overlap_cidr, normalize_port_range, is_port_in_range


class SecurityGroupRulePropertyType(Enum):
    SECURITY_GROUP_ID = ('UserIdGroupPairs', 'GroupId')
    IP_RANGES = ('IpRanges', 'CidrIp')
    PREFIX_LIST_ID = ('PrefixListIds', 'PrefixListId')


class ConnectionType(str, Enum):
    INBOUND = 'inbound'
    OUTBOUND = 'outbound'


class SecurityGroupRule(AwsResource):
    """
        Attributes:
            from_port: The bottom part of the port range the rule applies to.
            to_port: The top part of te port range the rule applies to.
            ip_protocol: The IP protocol used in the rule.
            property_type: The type of the rule, depending if it's targeting an IP
                destination, another security gruop, or a prefix list.
            property_value:
                If the type is SECURITY_GROUP_ID, then this is the GroupId.
                If the type is IP_RANGES, then this is the CIDR block.
                If the type is PREFIX_LIST_ID, then this is the Prefix List ID.
            has_description: True if the rule has a description set that is not
                a canned one (like "Managed by Terraform").
            connection_type: The type of the rule - inbound or outbound.
            security_group_id: The SG the rule belongs to.
    """

    def __init__(self, from_port: int, to_port: int, ip_protocol: IpProtocol, property_type: SecurityGroupRulePropertyType,
                 property_value: str, has_description: bool, connection_type: ConnectionType,
                 security_group_id: str, region: str, account: str):
        super().__init__(account, region, AwsServiceName.AWS_SECURITY_GROUP_RULE)
        normalized_from_port, normalized_to_port = normalize_port_range(from_port, to_port)
        self.from_port: int = normalized_from_port
        self.to_port: int = normalized_to_port
        self.ip_protocol: IpProtocol = ip_protocol
        self.property_type: SecurityGroupRulePropertyType = property_type
        self.property_value: str = property_value
        self.has_description: bool = has_description
        self.connection_type: ConnectionType = connection_type
        self.security_group_id: str = security_group_id

    def __str__(self) -> str:
        # todo - should return rule name in get id function
        return "SG permission: from_port={}, to_port={}, ip_protocol={}, property_type={}, property_value={}".format(
            self.from_port,
            self.to_port,
            self.ip_protocol,
            self.property_type.__str__(),
            self.property_value)

    def is_in_range(self, port: int) -> bool:
        return is_port_in_range((self.from_port, self.to_port), port)

    def get_keys(self) -> List[str]:
        return [self.security_group_id, self.from_port, self.to_port, self.ip_protocol,
                self.property_type, self.property_value, self.connection_type.value]

    def get_friendly_name(self) -> str:
        return '{} rule of {} for ports {}:{} using protocol {}' \
            .format('ingress' if self.connection_type == ConnectionType.INBOUND else 'egress',
                    self.property_value or self.security_group_id,
                    self.from_port,
                    self.to_port,
                    self.ip_protocol)

    def get_extra_data(self) -> str:
        return str(self)

    def is_match(self, rule: SecurityGroupRule) -> bool:
        # todo - need to support pl id type and cross account peering instance
        if self.ip_protocol == IpProtocol('ALL') or rule.ip_protocol == IpProtocol('ALL') or self.ip_protocol == rule.ip_protocol:
            is_ports_overlap: bool = get_range_numbers_overlap(self.get_ports_range(), rule.get_ports_range()) != EMPTY_RANGE
            if self.property_type == SecurityGroupRulePropertyType.SECURITY_GROUP_ID and self.property_value == rule.security_group_id:
                return is_ports_overlap
            elif rule.property_type == SecurityGroupRulePropertyType.IP_RANGES and \
                    get_overlap_cidr(rule.property_value, self.property_value).size > 0:
                return is_ports_overlap
        return False

    def get_ports_range(self) -> Tuple[int, int]:
        return self.from_port, self.to_port

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Security group rule'
        else:
            return 'Security group rules'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#SecurityGroup:groupId={2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.security_group_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False

    @staticmethod
    def is_standalone() -> bool:
        return False

    def to_drift_detection_object(self) -> dict:
        return {'from_port': self.from_port,
                'to_port': self.to_port,
                'ip_protocol': self.ip_protocol.__repr__(),
                'property_type': self.property_type.value,
                'property_value': self.property_value,
                'has_description': self.has_description,
                'connection_type': self.connection_type,
                'security_group_id': self.security_group_id}
