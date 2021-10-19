from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.azure.non_context_aware.defender_enabled_rules import SqlServersOnVirtualMachinesDefenderEnabledRule

from tests.knowledge.rules.base_rule_test import AzureBaseRuleTest, rule_test


class TestSqlServersOnVirtualMachinesDefenderEnabledRule(AzureBaseRuleTest):

    def get_rule(self):
        return SqlServersOnVirtualMachinesDefenderEnabledRule()

    @rule_test('defender_for_az_sql_vm_enabled', should_alert=False)
    def test_defender_for_container_registry_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('defender_for_az_sql_vm_disabled', should_alert=True)
    def test_defender_for_container_registry_disabled(self, rule_result: RuleResponse):
        pass
