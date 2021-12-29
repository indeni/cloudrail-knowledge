from unittest import TestCase
from parameterized import parameterized
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.resources.monitor.azure_activity_log_alert import AzureMonitorActivityLogAlert, MonitorActivityLogAlertCriteria, MonitorActivityLogAlertCriteriaCategory
from cloudrail.knowledge.context.azure.resources.subscription.azure_subscription import AzureSubscription
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.rules.azure.non_context_aware.monitor_activity_log_alert_exists_rule import NetworkSecurityGroupRulesMonitorActivityLogAlertExistsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestNetworkSecurityGroupRulesMonitorActivityLogAlertExistsRule(TestCase):
    def setUp(self):
        self.rule = NetworkSecurityGroupRulesMonitorActivityLogAlertExistsRule()

    @parameterized.expand(
        [
            ["Category missing", True, MonitorActivityLogAlertCriteriaCategory.RECOMMENDATION, True, 1, RuleResultType.FAILED],
            ["Monitor disabled", False, MonitorActivityLogAlertCriteriaCategory.ADMINISTRATIVE, True, 1, RuleResultType.FAILED],
            ["Monitor exists", True, MonitorActivityLogAlertCriteriaCategory.ADMINISTRATIVE, True, 0, RuleResultType.SUCCESS],
            ["Operation missing", True, MonitorActivityLogAlertCriteriaCategory.ADMINISTRATIVE, False, 1, RuleResultType.FAILED],
        ]
    )

    def test_network_security_group_rules_monitor_activity_log_alert_exists_rule(self, unused_name: str, enabled: bool, category: str, operations_name_exists: bool, total_issues: int, rule_status: RuleResultType):
        # Arrange
        subscription: AzureSubscription = create_empty_entity(AzureSubscription)
        monitors: AliasesDict[AzureMonitorActivityLogAlert] = AliasesDict()
        operations_name = self.rule._get_operations_name() if operations_name_exists else []
        for i in range(4):
            monitor = create_empty_entity(AzureMonitorActivityLogAlert)
            monitor.criteria = create_empty_entity(MonitorActivityLogAlertCriteria)
            monitor.criteria.operation_name = operations_name[i] if operations_name else None
            monitor.criteria.category = category
            monitor.enabled = enabled
            monitors.update(monitor)

        subscription.monitor_activity_alert_log_list = [monitor for monitor in monitors.values()]

        context = AzureEnvironmentContext(subscriptions=AliasesDict(subscription), monitor_activity_log_alert=monitors)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(rule_status, result.status)
        self.assertEqual(total_issues, len(result.issues))
