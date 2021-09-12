import unittest

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_acl import NetworkAcl
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc
from cloudrail.knowledge.context.aws.resources.es.elastic_search_domain import ElasticSearchDomain
from cloudrail.knowledge.context.aws.resources.indirect_public_connection_data import IndirectPublicConnectionData
from cloudrail.knowledge.rules.aws.context_aware.indirect_public_access_rules.indirect_public_access_elastic_search_rule import \
    IndirectPublicAccessElasticSearchRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestIndirectPublicAccessElasticSearchRule(unittest.TestCase):
    def setUp(self):
        self.rule = IndirectPublicAccessElasticSearchRule()
        self.security_group = create_empty_entity(SecurityGroup)
        self.ec2 = self._create_ec2()
        self.eni = self.ec2.network_resource.network_interfaces[0]

    def test_indirect_public_access_elastic_search_rule_fail(self):
        # Arrange
        es_domain = create_empty_entity(ElasticSearchDomain)
        es_domain.is_in_vpc = True
        es_domain.indirect_public_connection_data = IndirectPublicConnectionData(self.security_group, self.eni)
        es_domain.network_resource.add_interface(self.eni)
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_indirect_public_access_elastic_search_rule_pass(self):
        # Arrange
        es_domain = create_empty_entity(ElasticSearchDomain)
        es_domain.is_in_vpc = True
        context = AwsEnvironmentContext(elastic_search_domains=[es_domain])
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
        eni.subnet = create_empty_entity(Subnet)
        eni.subnet.vpc = create_empty_entity(Vpc)
        eni.subnet.name = 'subnet_name'
        eni.subnet.network_acl = create_empty_entity(NetworkAcl)
        eni.subnet.network_acl.name = 'acl_name'
        return ec2
