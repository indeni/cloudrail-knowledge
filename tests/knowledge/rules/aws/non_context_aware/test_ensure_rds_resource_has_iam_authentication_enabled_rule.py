import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.resources.rds.rds_cluster import RdsCluster
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_rds_resource_has_iam_authentication_enabled_rule import \
    EnsureRdsResourceIamAuthenticationEnabledRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureRdsResourceIamAuthenticationEnabledRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureRdsResourceIamAuthenticationEnabledRule()

    def test_non_car_rds_database_iam_authentication_enabled__supported_ver_no_auth__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.7.16'
        rds_instance.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__supported_ver_no_auth_8_0_17__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '8.0.17'
        rds_instance.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__supported_ver_no_auth_9_0_17__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '9.0.17'
        rds_instance.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__unsupported_version__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.7.15'
        rds_instance.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__unsupported_version_5_0_16_pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.0.16'
        rds_instance.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__unsupported_version_5_6_33__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.6.33'
        rds_instance.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__supported_version_auth_disabled__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.7'
        rds_instance.iam_database_authentication_enabled = False
        rds_instance.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__supported_version_auth_disabled_5_6__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'mysql'
        rds_instance.engine_version = '5.6'
        rds_instance.iam_database_authentication_enabled = False
        rds_instance.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_cluster__fail(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.engine_type = 'mysql'
        rds_cluster.engine_version = '5.7.mysql_aurora.2.03.2'
        rds_cluster.iam_database_authentication_enabled = False
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_cluster__pass(self):
        # Arrange
        rds_cluster: RdsCluster = create_empty_entity(RdsCluster)
        rds_cluster.engine_type = 'mysql'
        rds_cluster.engine_version = '5.7.mysql_aurora.2.03.2'
        rds_cluster.iam_database_authentication_enabled = True
        context = AwsEnvironmentContext(rds_clusters=[rds_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '9.5.16'
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_9_5__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '9.5'
        rds_instance.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_8_5__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '8.5'
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_11_2__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '11.2'
        rds_instance.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_14__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '14'
        rds_instance.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_14_5_non_tf__fail(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '14'
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_9_5_5_non_tf__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '9.5.5'
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_rds_database_iam_authentication_enabled__rds_instance_old_ver_9_5_5_tf__pass(self):
        # Arrange
        rds_instance: RdsInstance = create_empty_entity(RdsInstance)
        rds_instance.engine_type = 'postgresql'
        rds_instance.engine_version = '9.5.5'
        rds_instance.iac_state = IacState(address='address',
                                          action=TerraformActionType.CREATE,
                                          resource_metadata=None,
                                          is_new=True)
        context = AwsEnvironmentContext(rds_instances=[rds_instance])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
