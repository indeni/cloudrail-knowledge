import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.workspaces.workspaces import Workspace
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.\
    encrypt_at_rest.ensure_workspace_user_volume_encrypted_at_rest_rule import EnsureWorkspaceUserVolumeEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureWorkspaceUserVolumeEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureWorkspaceUserVolumeEncryptedAtRestRule()

    def test_non_car_workspace_user_volume_encrypt_at_rest_creating_fail(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = True
        workspace.user_encryption_enabled = False
        context = AwsEnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_workspace_user_volume_encrypt_at_rest_creating_pass(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = True
        workspace.user_encryption_enabled = True
        context = AwsEnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_workspace_user_volume_encrypt_at_rest_creating__not_new__pass(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = False
        workspace.user_encryption_enabled = False
        context = AwsEnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
