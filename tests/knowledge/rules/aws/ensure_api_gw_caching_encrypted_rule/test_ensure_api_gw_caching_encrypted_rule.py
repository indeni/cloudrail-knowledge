from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.ensure_api_gw_caching_encrypted_rule import EnsureApiGwCachingEncryptedRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureApiGwCachingEncryptedRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureApiGwCachingEncryptedRule()

    def test_encrypted_rest_api(self):
        self.run_test_case('encrypted_rest_api', False)

    def test_non_encrypted_rest_api_cache_enabled(self):
        self.run_test_case('non_encrypted_rest_api_cache_enabled', True)

    def test_non_encrypted_rest_api_cache_disabled(self):
        self.run_test_case('non_encrypted_rest_api_cache_disabled', False)
