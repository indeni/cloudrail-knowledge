import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.network.azure_network_interface import AzureNetworkInterface
from cloudrail.knowledge.context.azure.resources.network.azure_network_security_group import AzureNetworkSecurityGroup
from cloudrail.knowledge.context.azure.resources.network.azure_subnet import AzureSubnet
from cloudrail.knowledge.rules.azure.non_context_aware.unused_network_security_group_rule import UnusedNetworkSecurityGroupRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aliases_dict import AliasesDict


class TestUnusedNetworkSecurityGroupRule(unittest.TestCase):
    def setUp(self):
        self.rule = UnusedNetworkSecurityGroupRule()

    def test_non_car_unused_network_security_group_fail(self):
        # Arrange
        nsg = create_empty_entity(AzureNetworkSecurityGroup)
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(nsg))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_unused_network_security_group_pass_with_nic(self):
        # Arrange
        nsg = create_empty_entity(AzureNetworkSecurityGroup)
        nsg.network_interfaces = create_empty_entity(AzureNetworkInterface)
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(nsg))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unused_network_security_group_pass_with_subnet(self):
        # Arrange
        nsg = create_empty_entity(AzureNetworkSecurityGroup)
        nsg.subnets = create_empty_entity(AzureSubnet)
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(nsg))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unused_network_security_group_pass_with_nic_subnet(self):
        # Arrange
        nsg = create_empty_entity(AzureNetworkSecurityGroup)
        nsg.network_interfaces = create_empty_entity(AzureNetworkInterface)
        nsg.subnets = create_empty_entity(AzureSubnet)
        context = AzureEnvironmentContext(net_security_groups=AliasesDict(nsg))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
