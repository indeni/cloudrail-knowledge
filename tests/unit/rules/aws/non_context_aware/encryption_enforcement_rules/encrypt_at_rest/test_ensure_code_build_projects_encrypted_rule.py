import unittest

from cloudrail.knowledge.context.aws.resources.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_code_build_projects_encrypted_rule import \
    EnsureCodeBuildProjectsEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureCodeBuildProjectsEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCodeBuildProjectsEncryptedRule()

    def test_not_car_codebuild_projects_encrypted_at_rest_with_customer_managed_CMK_fail(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        codebuild_project.kms_data = kms_key
        context = AwsEnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_codebuild_projects_encrypted_at_rest_with_customer_managed_CMK_pass(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        codebuild_project.kms_data = kms_key
        context = AwsEnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
