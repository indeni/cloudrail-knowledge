import unittest

from cloudrail.dev_tools.aws_rule_test_utils import create_empty_network_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.eks.eks_cluster import EksCluster
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_eks_api_rule import PublicAccessEksApiRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessEksApiRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessEksApiRule()

    def test_public_access_eks_api_fail(self):
        # Arrange
        eks = create_empty_network_entity(EksCluster)
        security_group = create_empty_entity(SecurityGroup)
        eks.security_group_allowing_public_access = security_group
        context = AwsEnvironmentContext(eks_clusters=[eks], security_groups=AliasesDict(security_group))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_eks_api_pass(self):
        # Arrange
        eks = create_empty_network_entity(EksCluster)
        context = AwsEnvironmentContext(eks_clusters=[eks])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
