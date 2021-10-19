from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.ensure_api_gw_caching_encrypted_rule import EnsureApiGwCachingEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureApiGwCachingEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureApiGwCachingEncryptedRule()

    @rule_test('encrypted_rest_api', False)
    def test_encrypted_rest_api(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted_rest_api_cache_enabled', True)
    def test_non_encrypted_rest_api_cache_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('non_encrypted_rest_api_cache_disabled', False)
    def test_non_encrypted_rest_api_cache_disabled(self, rule_result: RuleResponse):
        pass
