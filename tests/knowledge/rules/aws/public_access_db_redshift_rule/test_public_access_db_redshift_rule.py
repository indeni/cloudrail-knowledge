from test.knowledge.rules.base_rule_test import AwsBaseRuleTest
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_redshift_rule import PublicAccessDbRedshiftRule


class PublicAccessDbRedshiftRuleTest(AwsBaseRuleTest):
    @classmethod
    def get_rule(cls):
        return PublicAccessDbRedshiftRule()

    def test_redshift_with_public_access(self):
        tf_use_case_folder_name = 'redshift_with_public_access'
        self.run_test_case(tf_use_case_folder_name, True)

    def test_redshift_without_public_access(self):
        tf_use_case_folder_name = 'redshift_without_public_access'
        self.run_test_case(tf_use_case_folder_name, False)
