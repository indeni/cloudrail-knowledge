from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.policy_wildcard_violation.ensure_glue_data_catalog_policy_not_use_wildcard_rule import \
    EnsureGlueDataCatalogPolicyNotUseWildcard
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureGlueDataCatalogPolicyNotUseWildcard(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureGlueDataCatalogPolicyNotUseWildcard()

    @rule_test('secure_policy', False)
    def test_secure_policy(self, rule_result: RuleResponse):
        pass

    @rule_test('not_secure_policy', True, 2)
    def test_not_secure_policy(self, rule_result: RuleResponse):
        self.assertIsNotNone(rule_result)
        for item in rule_result.issues:
            self.assertTrue("is using wildcard action `glue:*`, and principal `AWS: *`, without any condition" in item.evidence)
        table_exposed = next((item for item in rule_result.issues if item.exposed.get_type() == 'Glue Data Catalog table'))
        crawler_exposed = next((item for item in rule_result.issues if item.exposed.get_type() == 'Glue crawler'))
        self.assertIsNotNone(table_exposed)
        self.assertIsNotNone(crawler_exposed)
