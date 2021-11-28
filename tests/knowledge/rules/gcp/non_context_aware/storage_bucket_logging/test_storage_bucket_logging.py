from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.gcp.non_context_aware.storage_bucket_logging_enabled_rule import StorageBucketLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import GcpBaseRuleTest, rule_test


class TestStorageBucketLogging(GcpBaseRuleTest):

    def get_rule(self):
        return StorageBucketLoggingEnabledRule()

    @rule_test('bucket_logging_off', should_alert=True)
    def test_bucket_logging_off(self, rule_result: RuleResponse):
        pass

    @rule_test('bucket_logging_on', should_alert=False)
    def test_bucket_logging_on(self, rule_result: RuleResponse):
        pass
