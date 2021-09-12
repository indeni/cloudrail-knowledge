import unittest

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_rds_rule import IndirectPublicAccessDbRds
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIndirectPublicAccessDbRds(unittest.TestCase):
    def setUp(self):
        self.rule = IndirectPublicAccessDbRds()
        self.security_group = create_empty_entity(SecurityGroup)
        self.ec2 = self._create_ec2()

    def test_indirect_public_access_db_rds_fail_cluster(self):
        # Arrange
        rds_instance = self._create_instance(True)
        rds_cluster = self._create_cluster(rds_instance)
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster], rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_indirect_public_access_db_rds_fail_instance(self):
        # Arrange
        rds_instance = self._create_instance(True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_indirect_public_access_db_rds_fail_cluster_and_instance(self):
        # Arrange
        rds_instance_in_cluster = self._create_instance(True)
        rds_instance = self._create_instance(True)
        rds_cluster = self._create_cluster(rds_instance_in_cluster)
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster], rds_instances=[rds_instance_in_cluster, rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(2, len(result.issues))

    def test_indirect_public_access_db_rds_pass_cluster(self):
        # Arrange
        rds_instance = self._create_instance(False)
        rds_cluster = self._create_cluster(rds_instance)
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster], rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_indirect_public_access_db_rds_pass_instance(self):
        # Arrange
        rds_instance = self._create_instance(False)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    @staticmethod
    def _create_cluster(rds_instance: RdsInstance):
        rds_cluster = create_empty_entity(RdsCluster)
        rds_cluster.cluster_instances = [rds_instance]
        rds_cluster.cluster_id = 'cluster_id'
        rds_instance.db_cluster_id = 'cluster_iid'
        return rds_cluster

    def _create_instance(self, indirect_access: bool):
        rds_instance = create_empty_entity(RdsInstance)
        if indirect_access:
            rds_instance.indirect_public_connection_data = IndirectPublicConnectionData(self.security_group,
                                                                                        self.ec2.network_resource.network_interfaces[0])
        return rds_instance

    @staticmethod
    def _create_ec2():
        eni = create_empty_entity(NetworkInterface)
        ec2 = create_empty_entity(Ec2Instance)
        ec2.network_resource.add_interface(eni)
        eni.owner = ec2
        return ec2
