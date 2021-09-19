from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.iam_privilege_escalation_policy_rule import IamPrivilegeEscalationPolicyRule


class TestIamPrivilegeEscalationPolicyRule(AwsBaseRuleTest):

    def get_rule(self):
        return IamPrivilegeEscalationPolicyRule()

    def test_iam_all_resources(self):  # actions: "iam: AttachUser*", "ec2:createroute"
        rule_result = self.run_test_case('iam-all-resources', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('granting the problematic permissions' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_iam_role_policy.policy')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.resource_metadata.iac_entity_id, 'aws_iam_role_policy.policy')

    def test_escalation_permissions_denied(self):  # actions: "iam: AttachUserPolicy" (allow), "iam: AttachUser*" (deny)
        self.run_test_case('escalation-permissions-denied', False)

    def test_escalation_permissions_not_denied_resource_mismatch(self):  # actions: "iam:CreateAccessKey", resource: "*"
        rule_result = self.run_test_case('escalation-permissions-not-denied-resource-mismatch', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('granting the problematic permissions `{\'iam:CreateAccessKey\'}`' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'allow-policy')
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_iam_user_policy.allow-policy')

    def test_escalation_permissions_self_iam_entity_resource(self):  # actions: "iam:Create*", resource: associated group name
        self.run_test_case('escalation-permissions-self-iam-entity-resource', False)

    def test_none_escalation_permissions(self):  # actions: <some-none-escalation-permission>
        self.run_test_case('none-escalation-permissions', False)

    def test_not_associated_escalation_permissions(self):  # actions: "iam: *, policy not associated
        self.run_test_case('not-associated-escalation-permissions', False)

    def test_combo_escalation_permissions(self):  # actions: "iam: passrole", "lambda: createfunction", "lambda: invokefunc*"
        rule_result = self.run_test_case('combo-escalation-permissions', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue(all(item in rule_result.issues[0].evidence
                            for item in ("lambda: invokefunc*", "iam: passrole", "lambda: createfunction", "conjunction")))
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'allow-policy-1')
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_iam_role_policy.allow-policy-1')

    def test_combo_escalation_permissions_mismatch(self):  # actions: "lambda: createfunction", "lambda: invokefunc*"
        self.run_test_case('combo-escalation-permissions-mismatch', False)

    def test_iam_all_actions(self):  # actions: "*"
        rule_result = self.run_test_case('iam-all-actions', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("granting the problematic permissions `{\'*\'}` which can allow for privilege escalation"
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'allow-all-actions')
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_iam_role.role')

    def test_inline_policy_all_actions(self):
        rule_result = self.run_test_case('inline-policy-all-actions', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue("granting the problematic permissions `{\'*\'}` which can allow for privilege escalation"
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'ec2-describe-policy')
        self.assertEqual(rule_result.issues[0].violating.iac_state.resource_metadata.iac_entity_id, 'aws_iam_role.ec2-role')
