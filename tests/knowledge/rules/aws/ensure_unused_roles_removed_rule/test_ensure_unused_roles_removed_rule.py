from cloudrail.knowledge.rules.base_rule import RuleResponse
from unittest import skip

from cloudrail.knowledge.rules.aws.non_context_aware.ensure_unused_roles_removed_rule import EnsureUnusedRolesRemoved
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureUnusedRolesRemoved(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureUnusedRolesRemoved()

    @skip('skipped due to old data (more than 90 days')
    @rule_test('new_role_lately_used', False)
    def test_new_role_lately_used(self, rule_result: RuleResponse):
        pass

    @skip('skipped due to old data (more than 90 days')
    @rule_test('new_role_never_used', False)
    def test_new_role_never_used(self, rule_result: RuleResponse):
        pass

    @skip('skipped due to old data (more than 90 days')
    @rule_test('old_role_used_lately', False)
    def test_old_role_used_lately(self, rule_result: RuleResponse):
        pass

    @skip('skipped due to old data (more than 90 days')
    @rule_test('old_role_not_used_lately', True)
    def test_old_role_not_used_lately(self, rule_result: RuleResponse):
        pass

    @skip('skipped due to old data (more than 90 days')
    @rule_test('old_role_not_used_at_all', True)
    def test_old_role_not_used_at_all(self, rule_result: RuleResponse):
        pass
