import unittest

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.workspaces.workspaces import Workspace
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_workspace_root_volume_encrypted_with_customer_cmk_rule import \
    EnsureWorkspaceRootVolumeEncryptionCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureWorkspaceRootVolumeEncryptionCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureWorkspaceRootVolumeEncryptionCmkRule()

    def test_non_car_workspace_root_volume_encrypt_at_rest_with_customer_managed_CMK_creating_fail(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = True
        workspace.root_encryption_enabled = True
        workspace.keys_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.AWS, region='us-east-1', account='111111111')
        context = EnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_workspace_root_volume_encrypt_at_rest_with_customer_managed_CMK_creating_pass(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = True
        workspace.root_encryption_enabled = True
        workspace.keys_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_workspace_root_volume_encrypt_at_rest_with_customer_managed_CMK_creating__no_keys_data__pass(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = True
        workspace.root_encryption_enabled = True
        workspace.keys_data = None
        context = EnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_workspace_root_volume_encrypt_at_rest_with_customer_managed_CMK_creating__no_encrypt__pass(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = True
        workspace.root_encryption_enabled = False
        workspace.keys_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_workspace_root_volume_encrypt_at_rest_with_customer_managed_CMK_creating__not_new__pass(self):
        # Arrange
        workspace: Workspace = create_empty_entity(Workspace)
        terraform_state = create_empty_entity(TerraformState)
        workspace.terraform_state = terraform_state
        workspace.terraform_state.is_new = False
        workspace.root_encryption_enabled = True
        workspace.keys_data = KmsKey(key_id='key', arn='arn', key_manager=KeyManager.CUSTOMER, region='us-east-1', account='111111111')
        context = EnvironmentContext(workspaces=[workspace])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
