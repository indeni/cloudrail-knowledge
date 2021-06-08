import unittest
from typing import List

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.ecs.ecs_task_definition import EcsTaskDefinition, EfsVolume
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_action_type import TerraformActionType
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_in_transit.ensure_ecs_task_definition_created_with_efs_encrypt_in_transit_rule import\
    EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEcsTaskDefinitionCreatedWithEfsEncryptInTransitRule()

    def test_non_car_ecs_task_definition_encrypt_in_transit_with_efs_fail(self):
        # Arrange
        ecs_task_definition: EcsTaskDefinition = create_empty_entity(EcsTaskDefinition)
        ecs_task_definition.terraform_state = TerraformState(address='address', action=TerraformActionType.CREATE,
                                                             resource_metadata=None, is_new=True)
        efs_volume_data: List[EfsVolume] = [create_empty_entity(EfsVolume)]
        ecs_task_definition.efs_volume_data = efs_volume_data
        ecs_task_definition.is_volume_efs = True
        ecs_task_definition.family = 'efs_family'
        ecs_task_definition.efs_volume_data[0].encrypt_efs_in_transit = False
        ecs_task_definition.efs_volume_data[0].volume_name = 'efs_volume'
        context = AwsEnvironmentContext(ecs_task_definitions=[ecs_task_definition])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_ecs_task_definition_encrypt_in_transit_with_efs_pass(self):
        # Arrange
        ecs_task_definition: EcsTaskDefinition = create_empty_entity(EcsTaskDefinition)
        ecs_task_definition.terraform_state = TerraformState(address='address', action=TerraformActionType.CREATE,
                                                             resource_metadata=None, is_new=True)
        efs_volume_data: List[EfsVolume] = [create_empty_entity(EfsVolume)]
        ecs_task_definition.efs_volume_data = efs_volume_data
        ecs_task_definition.is_volume_efs = True
        ecs_task_definition.family = 'efs_family'
        ecs_task_definition.efs_volume_data[0].encrypt_efs_in_transit = True
        ecs_task_definition.efs_volume_data[0].volume_name = 'efs_volume'
        context = AwsEnvironmentContext(ecs_task_definitions=[ecs_task_definition])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_ecs_task_definition_encrypt_in_transit_with_efs__not_new__pass(self):
        # Arrange
        ecs_task_definition: EcsTaskDefinition = create_empty_entity(EcsTaskDefinition)
        ecs_task_definition.terraform_state = TerraformState(address='address', action=TerraformActionType.CREATE,
                                                             resource_metadata=None, is_new=False)
        efs_volume_data: List[EfsVolume] = [create_empty_entity(EfsVolume)]
        ecs_task_definition.efs_volume_data = efs_volume_data
        ecs_task_definition.is_volume_efs = True
        ecs_task_definition.family = 'efs_family'
        ecs_task_definition.efs_volume_data[0].encrypt_efs_in_transit = False
        ecs_task_definition.efs_volume_data[0].volume_name = 'efs_volume'
        context = AwsEnvironmentContext(ecs_task_definitions=[ecs_task_definition])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_ecs_task_definition_encrypt_in_transit_with_efs__not_efs__pass(self):
        # Arrange
        ecs_task_definition: EcsTaskDefinition = create_empty_entity(EcsTaskDefinition)
        ecs_task_definition.terraform_state = TerraformState(address='address', action=TerraformActionType.CREATE,
                                                             resource_metadata=None, is_new=True)
        efs_volume_data: List[EfsVolume] = [create_empty_entity(EfsVolume)]
        ecs_task_definition.efs_volume_data = efs_volume_data
        ecs_task_definition.is_volume_efs = False
        ecs_task_definition.family = 'efs_family'
        ecs_task_definition.efs_volume_data[0].encrypt_efs_in_transit = False
        ecs_task_definition.efs_volume_data[0].volume_name = 'efs_volume'
        context = AwsEnvironmentContext(ecs_task_definitions=[ecs_task_definition])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
