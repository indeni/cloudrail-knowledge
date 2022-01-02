from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.compute_instance_do_not_use_default_service_account_full_access_scope_rule import ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule(GcpBaseRuleTest):
    def get_rule(self):
        return ComputeInstanceDoNotUseDefaultServiceAccountFullAccessScopeRule()

    @rule_test('compute_instance_service_account_full_access_by_email_and_scope', should_alert=True)
    def test_compute_instance_service_account_full_access_by_email_and_scope(self, rule_result: RuleResponse):
        pass

    @rule_test('compute_instance_service_account_full_access_by_scope', should_alert=True)
    def test_compute_instance_service_account_full_access_by_scope(self, rule_result: RuleResponse):
        pass

    @rule_test('compute_instance_service_account_restricted_access', should_alert=False)
    def test_compute_instance_service_account_restricted_access(self, rule_result: RuleResponse):
        pass
