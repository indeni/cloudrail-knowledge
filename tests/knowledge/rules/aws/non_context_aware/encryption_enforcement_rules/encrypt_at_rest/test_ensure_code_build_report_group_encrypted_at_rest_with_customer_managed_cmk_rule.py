import unittest

from cloudrail.knowledge.context.aws.codebuild.codebuild_report_group import CodeBuildReportGroup
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_code_build_report_group_encrypted_at_rest_with_customer_managed_cmk_rule import \
    EnsureCodeBuildReportGroupEncryptedWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureCodeBuildReportGroupEncryptedWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCodeBuildReportGroupEncryptedWithCustomerManagedCmkRule()

    def test_not_car_codebuild_report_groups_encrypted_at_rest_with_customer_managed_cmk__export_config_s3_destination_kms_data_is_none__fail(self):
        # Arrange
        codebuild_report_group: CodeBuildReportGroup = create_empty_entity(CodeBuildReportGroup)
        codebuild_report_group.export_config_s3_destination_kms_data = None
        context = EnvironmentContext(codebuild_report_groups=[codebuild_report_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_codebuild_report_groups_encrypted_at_rest_with_customer_managed_cmk__kms_key_is_not_customer__fail(self):
        # Arrange
        codebuild_report_group: CodeBuildReportGroup = create_empty_entity(CodeBuildReportGroup)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        codebuild_report_group.export_config_s3_destination_kms_data = kms_key

        context = EnvironmentContext(codebuild_report_groups=[codebuild_report_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_codebuild_report_groups_encrypted_at_rest_with_customer_managed_cmk_pass(self):
        # Arrange
        codebuild_report_group: CodeBuildReportGroup = create_empty_entity(CodeBuildReportGroup)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        codebuild_report_group.export_config_s3_destination_kms_data = kms_key

        context = EnvironmentContext(codebuild_report_groups=[codebuild_report_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
