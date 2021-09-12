import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.account.account import Account
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.aws.resources.ec2.ec2_instance_type import EbsInfo, Ec2InstanceType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.performance_optimization.ensure_ec2_instance_ebs_optimized_rule import \
    EnsureEc2InstanceEbsOptimizedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureEc2InstanceEbsOptimizedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEc2InstanceEbsOptimizedRule()

    def test_non_car_ec2_instance_is_ebs_optimized_fail(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2_instance_type = Ec2InstanceType('t2.micro', EbsInfo('default', 'supported'))
        account: Account = create_empty_entity(Account)
        account.account = '11111111'
        ec2.instance_type = 't3.micro'
        ec2.ebs_optimized = False
        context = AwsEnvironmentContext(ec2s=[ec2], accounts=[account], ec2_instance_types=[ec2_instance_type])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ec2_instance_is_ebs_optimized__no_list_ebs_not_optimized__fail(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2_instance_type = Ec2InstanceType('t2.micro', EbsInfo('default', 'supported'))
        account: Account = create_empty_entity(Account)
        account.account = '11111111'
        ec2.instance_type = 't3.micro'
        ec2.ebs_optimized = False
        context = AwsEnvironmentContext(ec2s=[ec2], ec2_instance_types=[ec2_instance_type])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ec2_instance_is_ebs_optimized__in_list__pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2_instance_type = Ec2InstanceType('t2.micro', EbsInfo('default', 'supported'))
        account: Account = create_empty_entity(Account)
        account.account = '11111111'
        ec2.instance_type = 't2.micro'
        ec2.ebs_optimized = False
        context = AwsEnvironmentContext(ec2s=[ec2], accounts=[account], ec2_instance_types=[ec2_instance_type])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_ec2_instance_is_ebs_optimized__not_in_list_optimized__pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2_instance_type = Ec2InstanceType('t2.micro', EbsInfo('default', 'supported'))
        account: Account = create_empty_entity(Account)
        account.account = '11111111'
        ec2.instance_type = 't3.micro'
        ec2.ebs_optimized = True
        context = AwsEnvironmentContext(ec2s=[ec2], accounts=[account], ec2_instance_types=[ec2_instance_type])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_ec2_instance_is_ebs_optimized__no_list__pass(self):
        # Arrange
        ec2: Ec2Instance = create_empty_entity(Ec2Instance)
        ec2_instance_type = Ec2InstanceType('t2.micro', EbsInfo('default', 'supported'))
        account: Account = create_empty_entity(Account)
        account.account = '11111111'
        ec2.instance_type = 't3.micro'
        ec2.ebs_optimized = True
        context = AwsEnvironmentContext(ec2s=[ec2], ec2_instance_types=[ec2_instance_type])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
