import unittest

from cloudrail.dev_tools.aws_rule_test_utils import create_empty_network_entity
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_redshift_rule import PublicAccessDbRedshiftRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessDbRedshiftRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessDbRedshiftRule()

    def test_public_access_db_redshift_rule_fail(self):
        # Arrange
        redshift = create_empty_network_entity(RedshiftCluster)
        redshift.security_group_allowing_public_access = create_empty_entity(SecurityGroup)
        context = AwsEnvironmentContext(redshift_clusters=[redshift])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_db_redshift_rule_pass(self):
        # Arrange
        redshift = create_empty_network_entity(RedshiftCluster)
        context = AwsEnvironmentContext(redshift_clusters=[redshift])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
