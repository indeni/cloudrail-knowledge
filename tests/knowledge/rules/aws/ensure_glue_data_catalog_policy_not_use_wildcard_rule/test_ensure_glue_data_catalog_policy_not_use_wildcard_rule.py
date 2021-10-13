from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_glue_data_catalog_policy_not_use_wildcard_rule import \
    EnsureGlueDataCatalogPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureGlueDataCatalogPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureGlueDataCatalogPolicyNotUseWildcard()

    def test_secure_policy(self):
        self.run_test_case('secure_policy', False)

    def test_not_secure_policy(self):
        rule_result = self.run_test_case('not_secure_policy', True, 2)
        self.assertIsNotNone(rule_result)
        for item in rule_result.issues:
            self.assertTrue("is using wildcard action `glue:*`, and principal `AWS: *`, without any condition" in item.evidence)
        table_exposed = next((item for item in rule_result.issues if item.exposed.get_type() == 'Glue Data Catalog table'))
        crawler_exposed = next((item for item in rule_result.issues if item.exposed.get_type() == 'Glue crawler'))
        self.assertIsNotNone(table_exposed)
        self.assertIsNotNone(crawler_exposed)
