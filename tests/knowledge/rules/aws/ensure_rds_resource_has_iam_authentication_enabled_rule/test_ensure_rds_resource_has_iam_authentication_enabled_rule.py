from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rds_resource_has_iam_authentication_enabled_rule import \
    EnsureRdsResourceIamAuthenticationEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureRdsResourceIamAuthenticationEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureRdsResourceIamAuthenticationEnabledRule()

    def test_with_authentication(self):
        self.run_test_case('with_authentication', False)

    def test_without_authentication_supported_ver(self):
        self.run_test_case('without_authentication_supported', True, 2)

    def test_without_authentication_unsupported_ver(self):
        self.run_test_case('without_authentication_unsupported', False)
