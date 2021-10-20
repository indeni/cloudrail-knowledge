from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_security_group_include_description_rule import EnsureSecurityGroupIncludeDescriptionRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureSecurityGroupRuleIncludeDescriptionRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSecurityGroupIncludeDescriptionRule()

    @rule_test('description_exists', False)
    def test_description_exists(self, rule_result: RuleResponse):
        pass

    @rule_test('no_description_for_rules', True)
    def test_no_description_for_rules(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertEqual("The Security group `aws_security_group.default` "
                         "does not have a description for the `ingress rule of 10.0.0.0/24"
                         " for ports 443:443 using protocol TCP`", rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'examplerulename')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group rule')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_security_group.default')

    @rule_test('multiple_items_for_rules', True, 2)
    def test_multiple_items_for_rules(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        for item in rule_result.issues:
            self.assertTrue("does not have a description for the `ingress rule of" in item.evidence)
            self.assertEqual(item.exposed.get_type(), 'Security group')
            self.assertEqual(item.violating.get_type(), 'Security group rule')

    @rule_test('no_description_for_security_group', True)
    def test_no_description_for_security_group(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertEqual('The Security group `aws_security_group.default` does not have a non-default description',
                         rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'examplerulename')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'examplerulename')

    @rule_test('implicit_rule_without_description', True)
    def test_implicit_rule_without_description(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        self.assertTrue('The Security group `aws_security_group.instance` does not have a description for the `egress rule' in
                        rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'some-sg-name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group rule')

    @rule_test('implicit_rule_with_description', False)
    def test_implicit_rule_with_description(self, rule_result: RuleResponse):
        pass

    @rule_test('default_sg_no_description', False)
    def test_default_sg_no_description(self, rule_result: RuleResponse):
        pass
