from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_elasticsearch_domain_logging_enabled_rule import \
    EnsureElasticsearchDomainLoggingEnabledRule
from test.knowledge.rules.base_rule_test import AwsBaseRuleTest


class TestEnsureElasticsearchDomainLoggingEnabledRule(AwsBaseRuleTest):

    def get_rule(self):
        return EnsureElasticsearchDomainLoggingEnabledRule()

    def test_logging_enabled(self):
        self.run_test_case('logging_enabled', False)

    def test_logging_not_enabled(self):
        self.run_test_case('logging_not_enabled', True)

    def test_logging_not_enabled_no_block(self):
        self.run_test_case('logging_not_enabled_no_block', True)
