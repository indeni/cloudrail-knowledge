from cloudrail.knowledge.rules.aws.non_context_aware.ensure_security_group_include_description_rule import EnsureSecurityGroupIncludeDescriptionRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureSecurityGroupRuleIncludeDescriptionRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureSecurityGroupIncludeDescriptionRule()

    def test_description_exists(self):
        self.run_test_case('description_exists', False)

    def test_no_description_for_rules(self):
        rule_result = self.run_test_case('no_description_for_rules', True)
        self.assertIsNotNone(rule_result)
        self.assertEqual("The Security group `aws_security_group.default` "
                         "does not have a description for the `ingress rule of 10.0.0.0/24"
                         " for ports 443:443 using protocol TCP`", rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'examplerulename')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group rule')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_security_group.default')

    def test_multiple_items_for_rules(self):
        rule_result = self.run_test_case('multiple_items_for_rules', True, 2)
        self.assertIsNotNone(rule_result)
        for item in rule_result.issues:
            self.assertTrue("does not have a description for the `ingress rule of" in item.evidence)
            self.assertEqual(item.exposed.get_type(), 'Security group')
            self.assertEqual(item.violating.get_type(), 'Security group rule')

    def test_no_description_for_security_group(self):
        rule_result = self.run_test_case('no_description_for_security_group', True)
        self.assertIsNotNone(rule_result)
        self.assertEqual('The Security group `aws_security_group.default` does not have a non-default description',
                         rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'examplerulename')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'examplerulename')

    def test_implicit_rule_without_description(self):
        rule_result = self.run_test_case('implicit_rule_without_description', True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('The Security group `aws_security_group.instance` does not have a description for the `egress rule' in
                        rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Security group')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'some-sg-name')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Security group rule')

    def test_implicit_rule_with_description(self):
        self.run_test_case('implicit_rule_with_description', False)

    def test_default_sg_no_description(self):
        self.run_test_case('default_sg_no_description', False)
