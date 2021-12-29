from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.context_aware.storage_bucket_is_not_publicly_accessible_rule import StorageBucketIsNotPubliclyAccessibleRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestStorageBucketIsNotPubliclyAccessibleRule(GcpBaseRuleTest):
    def get_rule(self):
        return StorageBucketIsNotPubliclyAccessibleRule()

    @rule_test('storage_bucket_not_publicly_accesible_iam_binding', should_alert=False)
    def test_storage_bucket_not_publicly_accesible_iam_binding(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_bucket_not_publicly_accesible_iam_member', should_alert=False)
    def test_storage_bucket_not_publicly_accesible_iam_member(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_bucket_publicly_accessible_iam_binding_allAuthenticatedUsers', should_alert=True)
    def test_storage_bucket_publicly_accessible_iam_binding_all_authenticated_users(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_bucket_publicly_accessible_iam_binding_allUsers', should_alert=True)
    def test_storage_bucket_publicly_accessible_iam_binding_all_users(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_bucket_publicly_accessible_iam_member_allAuthenticatedUsers', should_alert=True)
    def test_storage_bucket_publicly_accessible_iam_member_all_authenticated_users(self, rule_result: RuleResponse):
        pass

    @rule_test('storage_bucket_publicly_accessible_iam_member_allUsers', should_alert=True)
    def test_storage_bucket_publicly_accessible_iam_member_all_users(self, rule_result: RuleResponse):
        pass
