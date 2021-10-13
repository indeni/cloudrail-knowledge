from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_policy_not_use_wildcard_actions_rules import \
    EnsureKmsKeyPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureKmsKeyPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureKmsKeyPolicyNotUseWildcard()

    def test_kms_key_not_secure_policy(self):
        rule_result = self.run_test_case('kms_key_not_secure_policy', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('is using wildcard action `kms:*`, and principal `AWS: *`, without any condition' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'KMS key')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'KMS key resource policy')

    def test_kms_key_secure_policy(self):
        self.run_test_case('kms_key_secure_policy', False)
