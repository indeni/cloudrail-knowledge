from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.s3_acl_allow_public_access_rule import S3AclAllowPublicAccessRule


class TestS3DisallowPublicAndCrossAccountRule(AwsBaseRuleTest):

    def get_rule(self):
        return S3AclAllowPublicAccessRule()

    @rule_test('acl_public_all_users_canned', True)
    def test_acl_public_all_users_canned(self, rule_result: RuleResponse):
        pass

    @rule_test('acl_public_all_authenticated_users_canned', True)
    def test_acl_public_all_authenticated_users_canned(self, rule_result: RuleResponse):
        pass

    @rule_test('test_acl_public_all_users_canned_with_overriding_access_block', False)
    def test_acl_public_all_users_canned_with_overriding_access_block(self, rule_result: RuleResponse):
        pass

    @rule_test('bucket_policy_public_to_all_users', True)
    def test_bucket_policy_public_to_all_users(self, rule_result: RuleResponse):
        pass

    @rule_test('bucket_policy_public_to_all_authenticated_users', True)
    def test_bucket_policy_public_to_all_authenticated_users(self, rule_result: RuleResponse):
        pass

    @rule_test('policy_public_but_access_block_applied', False)
    def test_policy_public_but_access_block_applied(self, rule_result: RuleResponse):
        pass

    @rule_test('cross_account_policy_over_privileged', False)
    def test_cross_account_policy_over_privileged(self, rule_result: RuleResponse):
        pass

    @rule_test('public_block_public_acls_and_deny_policy', False)
    def test_public_block_public_acls_and_deny_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('public_access_block_and_acls_allow_and_policy_deny', False)
    def test_public_access_block_and_acls_allow_and_policy_deny(self, rule_result: RuleResponse):
        pass

    @rule_test('default_bucket_settings', False)
    def test_default_bucket_settings(self, rule_result: RuleResponse):
        pass

    @rule_test('access-block-restrict-acl-and-read-write-acl-permissions', False)
    def test_access_block_restrict_acl_and_read_write_acl_permissions(self, rule_result: RuleResponse):
        pass

    @rule_test('unblock_public_access_with_no_policy', False)
    def test_unblock_public_access_with_no_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('unblock_public_access_with_policy', True)
    def test_unblock_public_access_with_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('restrict-public-access-block-and-full-access-policy', False)
    def test_restrict_public_access_block_and_full_access_policy(self, rule_result: RuleResponse):
        pass
