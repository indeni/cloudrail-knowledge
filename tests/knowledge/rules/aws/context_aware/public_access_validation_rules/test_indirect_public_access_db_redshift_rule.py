import unittest

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_db_redshift_rule import \
    IndirectPublicAccessDbRedshift
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIndirectPublicAccessDbRedshift(unittest.TestCase):
    def setUp(self):
        self.rule = IndirectPublicAccessDbRedshift()
        self.security_group = create_empty_entity(SecurityGroup)
        self.ec2 = self._create_ec2()
        self.eni = self.ec2.network_resource.network_interfaces[0]

    def test_indirect_public_access_db_redshift_fail(self):
        # Arrange
        redshift = create_empty_entity(RedshiftCluster)
        redshift.indirect_public_connection_data = IndirectPublicConnectionData(self.security_group, self.eni)
        context = AwsEnvironmentContext(redshift_clusters=[redshift])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_indirect_public_access_db_redshift_pass(self):
        # Arrange
        redshift = create_empty_entity(RedshiftCluster)
        context = AwsEnvironmentContext(redshift_clusters=[redshift])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    @staticmethod
    def _create_ec2():
        eni = create_empty_entity(NetworkInterface)
        ec2 = create_empty_entity(Ec2Instance)
        ec2.network_resource.add_interface(eni)
        eni.owner = ec2
        return ec2
