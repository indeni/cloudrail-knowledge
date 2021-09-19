from cloudrail.knowledge.rules.aws.context_aware.ensure_iam_entities_policy_managed_solely_rule import EnsureIamEntitiesPolicyManagedSolely
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureIamEntitiesPolicyManagedSolely(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureIamEntitiesPolicyManagedSolely()

    def test_role_managed_by_tf_alone(self):
        self.run_test_case('role_managed_by_tf_alone', False)

    def test_group_managed_by_tf_alone(self):
        self.run_test_case('group_managed_by_tf_alone', False)

    def test_user_managed_by_tf(self):
        self.run_test_case('user_managed_by_tf', False)

    def test_group_managed_by_tf_attached_policy_from_console(self):
        rule_result = self.run_test_case('group_managed_by_tf_attached_policy_from_console', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('AlexaForBusinessLifesizeDelegatedAccessPolicy' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'dev')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'AlexaForBusinessLifesizeDelegatedAccessPolicy')
        self.assertTrue(rule_result.issues[0].violating.get_type(), 'Managed Policy')

    def test_user_created_with_tf_managed_by_aws_console(self):
        rule_result = self.run_test_case('user_created_with_tf_managed_by_aws_console', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('AlexaForBusinessLifesizeDelegatedAccessPolicy' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Account')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Managed Policy')

    def test_user_managed_by_tf_attached_policy_from_group(self):
        rule_result = self.run_test_case('user_managed_by_tf_attached_policy_from_group', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('by adding it to the group' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'dev')

    def test_user_and_group_managed_by_tf_policy_attached_via_attaching_group_console(self):
        rule_result = self.run_test_case('policy_attached_via_attaching_group_console', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('by adding it to the group' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'dev')
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_iam_group.group')

    def test_role_managed_by_tf_attached_policy_from_console(self):
        rule_result = self.run_test_case('role_managed_by_tf_attached_policy_from_console', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('AlexaForBusinessGatewayExecution' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'dev')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'AlexaForBusinessGatewayExecution')
        self.assertTrue(rule_result.issues[0].violating.get_type(), 'Managed Policy')

    def test_group_and_user_managed_by_tf_managed_and_inline_policies_attached_from_console(self):
        self.run_test_case('inline_managed_attached_both_iac_and_AWS', True)
