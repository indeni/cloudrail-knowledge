from abc import abstractmethod
from typing import Union, List

from cloudrail.knowledge.context.aws.resources.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule, SecurityGroupRulePropertyType, ConnectionType
from cloudrail.knowledge.context.ip_protocol import IpProtocol

from cloudrail.knowledge.context.aws.resources_builders.cloudformation.base_cloudformation_builder import BaseCloudformationBuilder


class CloudformationSecurityGroupRuleBaseBuilder(BaseCloudformationBuilder):
    @abstractmethod
    def parse_resource(self, cfn_res_attr: dict) -> Union[AwsResource, List[AwsResource]]:
        pass

    @staticmethod
    def parse_security_group_rule(security_group_rule_properties: dict, egress: bool, security_group_id: str,
                                  account_id: str, region: str) -> SecurityGroupRule:
        conn_type: ConnectionType = ConnectionType.OUTBOUND if egress else ConnectionType.INBOUND
        sg_id_key: str = 'DestinationSecurityGroupId' if egress else 'SourceSecurityGroupId'
        pl_id_key: str = 'DestinationPrefixListId' if egress else 'SourcePrefixListId'
        target_type: SecurityGroupRulePropertyType
        rule_target: str
        ip_protocol = IpProtocol(BaseCloudformationBuilder.get_property(security_group_rule_properties, 'IpProtocol'))

        if ip_protocol == IpProtocol.ALL:
            from_port = 0
            to_port = 65535
        else:
            from_port = int(BaseCloudformationBuilder.get_property(security_group_rule_properties, 'FromPort', '-1'))
            to_port = int(BaseCloudformationBuilder.get_property(security_group_rule_properties, 'ToPort', '-1'))

        if 'CidrIp' in security_group_rule_properties or 'CidrIpv6' in security_group_rule_properties:
            target_type = SecurityGroupRulePropertyType.IP_RANGES
            rule_target = security_group_rule_properties.get('CidrIp') or security_group_rule_properties.get('CidrIpv6')
        elif sg_id_key in security_group_rule_properties:
            target_type = SecurityGroupRulePropertyType.SECURITY_GROUP_ID
            rule_target = security_group_rule_properties['DestinationSecurityGroupId']
        elif pl_id_key in security_group_rule_properties:
            target_type = SecurityGroupRulePropertyType.PREFIX_LIST_ID
            rule_target = security_group_rule_properties['DestinationPrefixListId']
        else:
            raise Exception(f'missing required properties for security group rule={str(security_group_rule_properties)}')
        return SecurityGroupRule(from_port=from_port,
                                 to_port=to_port,
                                 ip_protocol=ip_protocol,
                                 property_type=target_type,
                                 property_value=rule_target,
                                 has_description='Description' in security_group_rule_properties,
                                 connection_type=conn_type,
                                 security_group_id=security_group_id,
                                 region=region,
                                 account=account_id)
