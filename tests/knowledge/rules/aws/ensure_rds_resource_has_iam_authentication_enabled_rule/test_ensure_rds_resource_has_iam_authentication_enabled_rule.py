from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rds_resource_has_iam_authentication_enabled_rule import \
    EnsureRdsResourceIamAuthenticationEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureRdsResourceIamAuthenticationEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRdsResourceIamAuthenticationEnabledRule()

    @rule_test('with_authentication', False)
    def test_with_authentication(self, rule_result: RuleResponse):
        pass

    @rule_test('without_authentication_supported', True, 2)
    def test_without_authentication_supported_ver(self, rule_result: RuleResponse):
        pass

    @rule_test('without_authentication_unsupported', False)
    def test_without_authentication_unsupported_ver(self, rule_result: RuleResponse):
        pass
