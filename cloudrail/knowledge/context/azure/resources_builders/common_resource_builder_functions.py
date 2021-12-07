from dataclasses import dataclass
from typing import List, Optional

from cloudrail.knowledge.context.azure.resources.webapp.azure_identity import Identity
from cloudrail.knowledge.context.connection import ConnectionDirectionType
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group_rule import AzureNetworkSecurityRule, NetworkSecurityRuleActionType
from cloudrail.knowledge.context.ip_protocol import IpProtocol
from cloudrail.knowledge.utils.port_set import PortSet


@dataclass
class NetworkSecurityRuleTemplate:
    nsg_name: str
    rule_name: str
    priority: int
    acccess: str
    protocol: str
    direction: str
    destination_port_range: str
    destination_port_ranges: List[str]
    source_address_prefix: str
    source_address_prefixes: List[str]
    destination_address_prefix: str
    destination_address_prefixes: List[str]
    source_application_security_group_ids: List[str]
    destination_application_security_group_ids: List[str]


def create_network_security_rules(rule_templates: List[NetworkSecurityRuleTemplate]) -> List[AzureNetworkSecurityRule]:
    rules = []
    for rule_template in rule_templates:
        destination_port_ranges = PortSet([])
        if destination_port_range := rule_template.destination_port_range:
            if destination_port_range == '*':
                destination_port_ranges = PortSet.create_all_ports_set()
            else:
                destination_port_ranges.add(destination_port_range)
        else:
            destination_port_ranges.extend(rule_template.destination_port_ranges)

        rules.append(AzureNetworkSecurityRule(name=rule_template.rule_name,
                                              priority=rule_template.priority,
                                              direction=ConnectionDirectionType(rule_template.direction.lower()),
                                              access=NetworkSecurityRuleActionType(rule_template.acccess),
                                              protocol=IpProtocol(rule_template.protocol),
                                              destination_port_ranges=destination_port_ranges,
                                              source_address_prefixes=_build_address_prefixes(rule_template.source_address_prefix,
                                                                                              rule_template.source_address_prefixes),
                                              destination_address_prefixes=_build_address_prefixes(rule_template.destination_address_prefix,
                                                                                                   rule_template.destination_address_prefixes),
                                              network_security_group_name=rule_template.nsg_name,
                                              source_application_security_group_ids=rule_template.source_application_security_group_ids,
                                              destination_application_security_group_ids=rule_template.destination_application_security_group_ids))
    return rules


def _build_address_prefixes(single_address_prefix: Optional[str], multiple_address_prefixes: List[str]):
    addresses = []
    if single_address_prefix:
        addresses.extend(_build_address_prefix(single_address_prefix))
    if multiple_address_prefixes:
        for prefix in multiple_address_prefixes:
            addresses.extend(_build_address_prefix(prefix))

    return addresses

def _build_address_prefix(prefix: str):
    addresses = []
    if prefix in ('*', 'Internet'):
        addresses.append('0.0.0.0/0')
        addresses.append('::/0')
    else:
        addresses.append(prefix)
    return addresses


def _build_scanner_identity(attributes):
    identity = None
    if identity_data := attributes.get('identity'):
        identity_ids = []
        if identity_data.get('type') == 'UserAssigned':
            identity_ids = identity_data.get('userAssignedIdentities')
        elif identity_data.get('type') == 'SystemAssigned':
            if identity_data.get('tenantId'):
                identity_ids.append(identity_data.get('tenantId'))
            if identity_data.get('principalId'):
                identity_ids.append(identity_data.get('principalId'))
        identity = Identity(type=identity_data.get('type'),
                            identity_ids=identity_ids)
    return identity
