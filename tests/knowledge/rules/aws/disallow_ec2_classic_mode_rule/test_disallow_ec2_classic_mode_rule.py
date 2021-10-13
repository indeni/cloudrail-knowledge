from cloudrail.knowledge.rules.aws.context_aware.disallow_ec2_classic_mode_rule import DisallowEc2ClassicModeRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class DisallowEc2ClassicModeRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return DisallowEc2ClassicModeRule()

    def test_deploy_redshift_in_ec2_vpc_mode(self):
        tf_use_case_folder_name = 'deploy_redshift_in_ec2_vpc_mode'
        self.run_test_case(tf_use_case_folder_name, False)

    def test_deploy_redshift_in_ec2_classic_mode(self):
        tf_use_case_folder_name = 'deploy_redshift_in_ec2_classic_mode'
        self.run_test_case(tf_use_case_folder_name)
