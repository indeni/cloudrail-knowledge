from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.non_context_aware.protocol_enforcments.ensure_imdsv2_is_used_rule import EnsureImdsv2IsUsedRule


class EnsureImdsv2IsUsedRuleTest(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureImdsv2IsUsedRule()

    def test_ec2_http_tokens_optional(self):
        tf_use_case_folder_name = 'ec2_http_tokens_optional'
        rule_result = self.run_test_case(tf_use_case_folder_name, True)
        self.assertIsNotNone(rule_result)
        self.assertTrue('The EC2 Instance `aws_instance.t2-instance` is allowing IMDSv1' in rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].exposed.get_name(), 'aws_instance.t2-instance.id')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'EC2 Instance')
        self.assertEqual(rule_result.issues[0].violating.get_name(), 'aws_instance.t2-instance.id')

    def test_ec2_http_tokens_required(self):
        tf_use_case_folder_name = 'ec2_http_tokens_required'
        self.run_test_case(tf_use_case_folder_name, False)

    def test_launch_configurations_optional(self):
        tf_use_case_folder_name = 'launch_configurations_optional'
        rule_result = self.run_test_case(tf_use_case_folder_name, True)
        self.assertIsNotNone(rule_result)
        self.assertEqual('The Launch configuration `aws_launch_configuration.as_conf` is allowing IMDSv1', rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Launch configuration')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_launch_configuration.as_conf')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Launch configuration')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_launch_configuration.as_conf')

    def test_launch_templates_http_token_optional(self):
        tf_use_case_folder_name = 'launch_templates_http_token_optional'
        rule_result = self.run_test_case(tf_use_case_folder_name, True)
        self.assertIsNotNone(rule_result)
        self.assertEqual('The Launch template `aws_launch_template.launch_template_test` is allowing IMDSv1', rule_result.issues[0].evidence)
        self.assertEqual(rule_result.issues[0].exposed.get_type(), 'Launch template')
        self.assertEqual(rule_result.issues[0].exposed.iac_state.address, 'aws_launch_template.launch_template_test')
        self.assertEqual(rule_result.issues[0].violating.get_type(), 'Launch template')
        self.assertEqual(rule_result.issues[0].violating.iac_state.address, 'aws_launch_template.launch_template_test')

    def test_launch_templates_http_token_required(self):
        tf_use_case_folder_name = 'launch_templates_http_token_required'
        self.run_test_case(tf_use_case_folder_name, False)
