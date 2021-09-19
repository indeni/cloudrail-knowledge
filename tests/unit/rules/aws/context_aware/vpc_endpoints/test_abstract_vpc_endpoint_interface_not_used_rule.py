import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.context_aware.vpc_endpoints.abstract_vpc_endpoint_interface_not_used_rule import Ec2VpcEndpointExposureRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.connection import ConnectionDirectionType, PolicyConnectionProperty, PublicConnectionDetail
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc


class TestEc2VpcEndpointExposureRule(unittest.TestCase):
    def setUp(self):
        self.rule = Ec2VpcEndpointExposureRule()

    def test_vpc_endpoint_ec2_exposure_fail(self):
        # Arrange
        default_region = 'us-east-1'
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.region = default_region
        vpc: Vpc = create_empty_entity(Vpc)
        vpc.region = default_region
        vpc.with_aliases('vpc-alias')
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        subnet: Subnet = create_empty_entity(Subnet)
        subnet.vpc_id = 'vpc-alias'
        subnet.vpc = vpc
        network_interface.subnet = subnet
        network_interface.owner = ec2
        connection_detail = PublicConnectionDetail(PolicyConnectionProperty([]), ConnectionDirectionType.OUTBOUND)
        network_interface.outbound_connections.add(connection_detail)
        context = AwsEnvironmentContext(vpcs=AliasesDict(vpc),
                                        ec2s=[ec2],
                                        subnets=AliasesDict(subnet),
                                        network_interfaces=AliasesDict(network_interface))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_vpc_endpoint_ec2_exposure_pass(self):
        # Arrange
        default_region = 'us-east-1'
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2.region = default_region
        vpc: Vpc = create_empty_entity(Vpc)
        vpc.with_aliases('vpc-alias')
        vpc.region = default_region
        network_interface: NetworkInterface = create_empty_entity(NetworkInterface)
        subnet: Subnet = create_empty_entity(Subnet)
        subnet.vpc_id = 'vpc-alias'
        subnet.vpc = vpc
        network_interface.subnet = subnet
        network_interface.owner = ec2
        context = AwsEnvironmentContext(vpcs=AliasesDict(vpc),
                                        ec2s=[ec2],
                                        subnets=AliasesDict(subnet),
                                        network_interfaces=AliasesDict(network_interface))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
