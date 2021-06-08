import unittest

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_efs_filesystems_encrypted_at_rest_rule \
    import EnsureEfsFilesystemsEncryptedAtRestRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aws.efs.efs_file_system import ElasticFileSystem


class TestEnsureEfsFilesystemsEncryptedAtRestRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureEfsFilesystemsEncryptedAtRestRule()

    def test_non_car_efs_filesystem_encrypt_at_rest_creating_fail(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        terraform_state = create_empty_entity(TerraformState)
        efs.terraform_state = terraform_state
        efs.terraform_state.is_new = True
        efs.encrypted = False

        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_efs_filesystem_encrypt_at_rest_creating__encrypted__pass(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        terraform_state = create_empty_entity(TerraformState)
        efs.terraform_state = terraform_state
        efs.terraform_state.is_new = True
        efs.encrypted = True

        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_efs_filesystem_encrypt_at_rest_creating_not_new_resource__pass(self):
        # Arrange
        efs: ElasticFileSystem = create_empty_entity(ElasticFileSystem)
        terraform_state = create_empty_entity(TerraformState)
        efs.terraform_state = terraform_state
        efs.terraform_state.is_new = True
        efs.encrypted = True

        context = AwsEnvironmentContext(efs_file_systems=[efs])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
