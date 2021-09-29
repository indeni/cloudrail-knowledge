import json
import pathlib

from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.security_group_rule import SecurityGroupRule, SecurityGroupRulePropertyType, ConnectionType
from cloudrail.knowledge.context.aws.resources.iam.policy import ManagedPolicy
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import PolicyStatement, StatementEffect
from cloudrail.knowledge.context.aws.resources.iam.principal import Principal, PrincipalType
from cloudrail.knowledge.context.ip_protocol import IpProtocol


def get_all_inclusive_security_group(account: str, region: str) -> SecurityGroup:
    all_inclusive_inbound_ipv4_permission = SecurityGroupRule(0, 65535, IpProtocol('ALL'), SecurityGroupRulePropertyType.IP_RANGES,
                                                              '0.0.0.0/0', True, ConnectionType.INBOUND,
                                                              'AllInclusiveSecurityGroup', region, account)
    all_inclusive_outbound_ipv4_permission = SecurityGroupRule(0, 65535, IpProtocol('ALL'),
                                                               SecurityGroupRulePropertyType.IP_RANGES, '0.0.0.0/0', True,
                                                               ConnectionType.OUTBOUND, 'AllInclusiveSecurityGroup', region, account)
    all_inclusive_inbound_ipv6_permission = SecurityGroupRule(0, 65535, IpProtocol('ALL'), SecurityGroupRulePropertyType.IP_RANGES,
                                                              '::/0', True,
                                                              ConnectionType.INBOUND, 'AllInclusiveSecurityGroup', region, account)
    all_inclusive_outbound_ipv6_permission = SecurityGroupRule(0, 65535, IpProtocol('ALL'),
                                                               SecurityGroupRulePropertyType.IP_RANGES, '::/0', True,
                                                               ConnectionType.OUTBOUND, 'AllInclusiveSecurityGroup', region, account)
    all_inclusive_security_group = SecurityGroup('AllInclusiveSecurityGroup', 'fake-region', account,
                                                 'AllInclusiveSecurityGroup', None, False, True)
    all_inclusive_security_group.inbound_permissions = [all_inclusive_inbound_ipv4_permission,
                                                        all_inclusive_inbound_ipv6_permission]
    all_inclusive_security_group.outbound_permissions = [all_inclusive_outbound_ipv4_permission,
                                                         all_inclusive_outbound_ipv6_permission]
    return all_inclusive_security_group


def _base_read_only_policy() -> ManagedPolicy:
    file_path = pathlib.Path(__file__).parent / 'policy/known_policies_statements.json'
    with open(file_path) as file:
        actions_policy_list = json.load(file)['ReadOnlyAccess']
    policy_statements = [PolicyStatement(StatementEffect.ALLOW, actions_policy_list,
                                         ['*'], Principal(PrincipalType.PUBLIC, ['*']))]
    return ManagedPolicy('11111111', 'ANPAILL3HVNFSB6DCOWYQ', 'ReadOnlyAccess',
                         'arn:aws:iam::aws:policy/ReadOnlyAccess', policy_statements, None)


_readonly_policy = _base_read_only_policy()


def get_readonly_policy(account_id: str):
    policy = _readonly_policy
    policy.account = account_id
    return policy


def get_empty_extended_environment_context():
    return None
