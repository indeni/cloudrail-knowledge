import unittest

from cloudrail.dev_tools.aws_rule_test_utils import create_empty_network_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.neptune.neptune_cluster import NeptuneCluster
from cloudrail.knowledge.context.aws.resources.neptune.neptune_instance import NeptuneInstance
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_neptune_rule import PublicAccessDbNeptuneRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessDbNeptuneRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessDbNeptuneRule()

    def test_public_access_db_neptune_fail(self):
        # Arrange
        neptune_cluster = create_empty_entity(NeptuneCluster)
        neptune_instance = create_empty_network_entity(NeptuneInstance)
        neptune_cluster.cluster_instances.append(neptune_instance)
        security_group = create_empty_entity(SecurityGroup)
        neptune_instance.security_group_allowing_public_access = security_group

        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster], neptune_cluster_instances=[neptune_instance],
                                        security_groups=AliasesDict(security_group))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_db_neptune_pass(self):
        # Arrange
        neptune_cluster = create_empty_entity(NeptuneCluster)
        neptune_instance = create_empty_network_entity(NeptuneInstance)
        neptune_cluster.cluster_instances.append(neptune_instance)

        context = AwsEnvironmentContext(neptune_clusters=[neptune_cluster], neptune_cluster_instances=[neptune_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
