from unittest import skip

from cloudrail.knowledge.rules.aws.non_context_aware.ensure_unused_roles_removed_rule import EnsureUnusedRolesRemoved
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureUnusedRolesRemoved(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureUnusedRolesRemoved()

    @skip('skipped due to old data (more than 90 days')
    def test_new_role_lately_used(self):
        self.run_test_case('new_role_lately_used', False)

    @skip('skipped due to old data (more than 90 days')
    def test_new_role_never_used(self):
        self.run_test_case('new_role_never_used', False)

    @skip('skipped due to old data (more than 90 days')
    def test_old_role_used_lately(self):
        self.run_test_case('old_role_used_lately', False)

    @skip('skipped due to old data (more than 90 days')
    def test_old_role_not_used_lately(self):
        self.run_test_case('old_role_not_used_lately', True)

    @skip('skipped due to old data (more than 90 days')
    def test_old_role_not_used_at_all(self):
        self.run_test_case('old_role_not_used_at_all', True)
