import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.security.azure_security_center_auto_provisioning import AzureSecurityCenterAutoProvisioning
from cloudrail.knowledge.rules.azure.non_context_aware.auto_provisioning_log_analytics_agent_disabled_rule import \
    AutoProvisioningLogAnalyticsAgentDisabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestAutoProvisioningLogAnalyticsAgentDisabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = AutoProvisioningLogAnalyticsAgentDisabledRule()

    def test_auto_provisioning_log_analytics_agent_disabled_pass(self):
        # Arrange
        scap = create_empty_entity(AzureSecurityCenterAutoProvisioning)
        scap.auto_provision_is_on = False
        context = AzureEnvironmentContext(security_center_auto_provisioning=AliasesDict(scap))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_unused_network_security_group_pass_with_nic(self):
        # Arrange
        scap = create_empty_entity(AzureSecurityCenterAutoProvisioning)
        scap.auto_provision_is_on = True
        context = AzureEnvironmentContext(security_center_auto_provisioning=AliasesDict(scap))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
