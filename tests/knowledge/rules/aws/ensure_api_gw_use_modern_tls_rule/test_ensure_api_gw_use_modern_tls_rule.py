from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_api_gw_use_modern_tls_rule import EnsureApiGwUseModernTlsRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureApiGwUseModernTlsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureApiGwUseModernTlsRule()

    @rule_test('tls_good_encryption', False)
    def test_tls_good_encryption(self, rule_result: RuleResponse):
        pass

    @rule_test('tls_bad_encryption', True)
    def test_tls_bad_encryption(self, rule_result: RuleResponse):
        pass
