from cloudrail.knowledge.rules.base_rule import RuleResponse
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test
from cloudrail.knowledge.rules.aws.context_aware.iam_privilege_escalation_policy_rule import IamPrivilegeEscalationPolicyRule


class TestIamPrivilegeEscalationPolicyRule(AwsBaseRuleTest):

    def get_rule(self):
        return IamPrivilegeEscalationPolicyRule()

    @rule_test('iam-all-resources', True)
    def test_iam_all_resources(self, rule_result: RuleResponse):  # actions: "iam: AttachUser*", "ec2:createroute"
        self.assertIsNotNone(rule_result)
        self.assertTrue('granting the problematic permissions' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_role_policy.policy')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_iam_role_policy.policy')

    @rule_test('escalation-permissions-denied', False)
    def test_escalation_permissions_denied(self, rule_result: RuleResponse):  # actions: "iam: AttachUserPolicy" (allow), "iam: AttachUser*" (deny)
        pass

    @rule_test('escalation-permissions-not-denied-resource-mismatch', True)
    def test_escalation_permissions_not_denied_resource_mismatch(self, rule_result: RuleResponse):  # actions: "iam:CreateAccessKey", resource: "*"
        self.assertIsNotNone(rule_result)
        self.assertTrue('granting the problematic permissions `{\'iam:CreateAccessKey\'}`' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'allow-policy')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_user_policy.allow-policy')

    @rule_test('escalation-permissions-self-iam-entity-resource', False)
    def test_escalation_permissions_self_iam_entity_resource(self, rule_result: RuleResponse):  # actions: "iam:Create*", resource: associated group name
        pass

    @rule_test('none-escalation-permissions', False)
    def test_none_escalation_permissions(self, rule_result: RuleResponse):  # actions: <some-none-escalation-permission>
        pass

    @rule_test('not-associated-escalation-permissions', False)
    def test_not_associated_escalation_permissions(self, rule_result: RuleResponse):  # actions: "iam: *, policy not associated
        pass

    @rule_test('combo-escalation-permissions', True)
    def test_combo_escalation_permissions(self, rule_result: RuleResponse):  # actions: "iam: passrole", "lambda: createfunction", "lambda: invokefunc*"
        self.assertIsNotNone(rule_result)
        self.assertTrue(all(item in rule_result.issues[0].evidence
                            for item in ("lambda: invokefunc*", "iam: passrole", "lambda: createfunction", "conjunction")))
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'allow-policy-1')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_role_policy.allow-policy-1')

    @rule_test('combo-escalation-permissions-mismatch', False)
    def test_combo_escalation_permissions_mismatch(self, rule_result: RuleResponse):  # actions: "lambda: createfunction", "lambda: invokefunc*"
        pass

    @rule_test('iam-all-actions', True)
    def test_iam_all_actions(self, rule_result: RuleResponse):  # actions: "*"
        self.assertIsNotNone(rule_result)
        self.assertTrue("granting the problematic permissions `{\'*\'}` which can allow for privilege escalation"
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'allow-all-actions')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_role.role')

    @rule_test('inline-policy-all-actions', True)
    def test_inline_policy_all_actions(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue("granting the problematic permissions `{\'*\'}` which can allow for privilege escalation"
                        in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'ec2-describe-policy')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_iam_role.ec2-role')
