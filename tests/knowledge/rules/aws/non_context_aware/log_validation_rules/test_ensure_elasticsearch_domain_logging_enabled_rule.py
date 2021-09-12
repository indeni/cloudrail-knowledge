import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain, LogPublishingOptions
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.log_validation_rules.ensure_elasticsearch_domain_logging_enabled_rule import \
    EnsureElasticsearchDomainLoggingEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureElasticsearchDomainLoggingEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureElasticsearchDomainLoggingEnabledRule()

    def test_non_car_elasticsearch_domain_logging_enabled__log_exists_not_enabled__fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        log_publish_options: LogPublishingOptions = create_empty_entity(LogPublishingOptions)
        log_publish_options.enabled = False
        log_publish_options.log_type = 'Some_type'
        es_domain.log_publishing_options = [log_publish_options]
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue('does not have logging enabled for log type' in result.issues[0].evidence)

    def test_non_car_elasticsearch_domain_logging_enabled__no_login_configured__fail(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        es_domain.log_publishing_options = []
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertTrue('does not have logging configured at all' in result.issues[0].evidence)

    def test_non_car_elasticsearch_domain_logging_enabled_pass(self):
        # Arrange
        es_domain: ElasticSearchDomain = create_empty_entity(ElasticSearchDomain)
        log_publish_options: LogPublishingOptions = create_empty_entity(LogPublishingOptions)
        log_publish_options.enabled = True
        log_publish_options.log_type = 'Some_type'
        es_domain.log_publishing_options = [log_publish_options]
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
