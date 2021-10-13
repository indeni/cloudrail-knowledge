from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_api_gw_use_modern_tls_rule import EnsureApiGwUseModernTlsRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureApiGwUseModernTlsRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureApiGwUseModernTlsRule()

    def test_tls_good_encryption(self):
        self.run_test_case('tls_good_encryption', False)

    def test_tls_bad_encryption(self):
        self.run_test_case('tls_bad_encryption', True)
