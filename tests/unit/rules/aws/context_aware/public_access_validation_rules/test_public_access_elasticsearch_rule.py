import unittest

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_elasticsearch_rule import PublicAccessElasticSearchRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessElasticSearchRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessElasticSearchRule()

    def test_public_access_elasticsearch_rule_fail(self):
        # Arrange
        es_domain = create_empty_entity(ElasticSearchDomain)
        es_domain.is_public = True
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_elasticsearch_rule_pass(self):
        # Arrange
        es_domain = create_empty_entity(ElasticSearchDomain)
        es_domain.is_public = False
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
