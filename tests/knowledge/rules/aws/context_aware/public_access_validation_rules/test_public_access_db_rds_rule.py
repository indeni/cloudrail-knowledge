import unittest

from cloudrail.dev_tools.aws_rule_test_utils import create_empty_network_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.rules.aws.context_aware.public_access_validation_rules.public_access_db_rds_rule import PublicAccessDbRdsRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestPublicAccessDbRdsRule(unittest.TestCase):
    def setUp(self):
        self.rule = PublicAccessDbRdsRule()

    def test_public_access_db_rds_rule_fail_cluster(self):
        # Arrange
        context = self._create_context(True, True)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_db_rds_rule_fail_instance(self):
        # Arrange
        context = self._create_context(False, True)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_public_access_db_rds_rule_pass_instance(self):
        # Arrange
        context = self._create_context(False, False)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_public_access_db_rds_rule_pass_cluster(self):
        # Arrange
        context = self._create_context(False, False)
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    @staticmethod
    def _create_context(with_cluster: bool, with_violating_sg: bool):
        rds_instance = create_empty_network_entity(RdsInstance)
        security_group = create_empty_entity(SecurityGroup)
        if with_violating_sg:
            rds_instance.security_group_allowing_public_access = security_group
        if with_cluster:
            rds_cluster = create_empty_entity(RdsCluster)
            rds_cluster.cluster_instances.append(rds_instance)
            rds_cluster.cluster_id = 'db_cluster_id'
            rds_instance.db_cluster_id = 'db_cluster_id'
        return AwsEnvironmentContext(rds_clusters=[rds_cluster] if with_cluster else [],
                                     rds_instances=[rds_instance],
                                     security_groups=AliasesDict(security_group) if with_violating_sg else [])
