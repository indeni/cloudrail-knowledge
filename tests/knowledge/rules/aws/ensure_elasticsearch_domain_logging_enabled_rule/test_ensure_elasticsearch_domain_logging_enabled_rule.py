from cloudrail.knowledge.rules.base_rule import RuleResponse
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_elasticsearch_domain_logging_enabled_rule import \
    EnsureElasticsearchDomainLoggingEnabledRule
from tests.knowledge.rules.base_rule_test import AwsBaseRuleTest, rule_test


class TestEnsureElasticsearchDomainLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticsearchDomainLoggingEnabledRule()

    @rule_test('logging_enabled', False)
    def test_logging_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('logging_not_enabled', True)
    def test_logging_not_enabled(self, rule_result: RuleResponse):
        pass

    @rule_test('logging_not_enabled_no_block', True)
    def test_logging_not_enabled_no_block(self, rule_result: RuleResponse):
        pass
