from cloudrail.knowledge.rules.aws.context_aware.ec2_role_share_rule import Ec2RoleShareRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class Ec2RoleShareRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return Ec2RoleShareRule()

    def test_public_and_private_ec2_same_role(self):
        tf_use_case_folder_name = 'public_and_private_ec2_same_role'
        self.run_test_case(tf_use_case_folder_name, True)

    def test_public_and_private_ec2_different_role(self):
        tf_use_case_folder_name = 'public_and_private_ec2_different_role'
        self.run_test_case(tf_use_case_folder_name, False)

    def test_public_and_public_ec2_same_role(self):
        tf_use_case_folder_name = 'public_and_public_ec2_same_role'
        self.run_test_case(tf_use_case_folder_name, False)

    def test_private_and_private_ec2_same_role(self):
        tf_use_case_folder_name = 'private_and_private_ec2_same_role'
        self.run_test_case(tf_use_case_folder_name, False)
