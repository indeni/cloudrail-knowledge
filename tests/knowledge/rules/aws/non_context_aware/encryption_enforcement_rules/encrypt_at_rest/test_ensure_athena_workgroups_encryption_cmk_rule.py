import unittest

from cloudrail.knowledge.context.aws.resources.athena.athena_workgroup import AthenaWorkgroup
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_action_type import IacActionType
from cloudrail.knowledge.context.iac_state import IacState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_athena_workgroups_encryption_cmk_rule import \
    EnsureAthenaWorkgroupsEncryptionCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureAthenaWorkgroupsEncryptionCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureAthenaWorkgroupsEncryptionCmkRule()

    def test_non_car_athena_workgroup_query_results_encrypt_at_rest_using_customer_managed_cmk__encryption_option_is_SSE_S3__fail(self):
        # Arrange
        athena_workgroup: AthenaWorkgroup = create_empty_entity(AthenaWorkgroup)
        athena_workgroup.iac_state = IacState(address='address',
                                              action=IacActionType.CREATE,
                                              resource_metadata=None,
                                              is_new=True)
        athena_workgroup.encryption_option = 'SSE_S3'

        context = AwsEnvironmentContext(athena_workgroups=[athena_workgroup])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_athena_workgroup_query_results_encrypt_at_rest_using_customer_managed_cmk__key_manager_is_not_customer__fail(self):
        # Arrange
        athena_workgroup: AthenaWorkgroup = create_empty_entity(AthenaWorkgroup)
        athena_workgroup.iac_state = IacState(address='address',
                                              action=IacActionType.CREATE,
                                              resource_metadata=None,
                                              is_new=True)
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        athena_workgroup.kms_data = kms_key

        context = AwsEnvironmentContext(athena_workgroups=[athena_workgroup])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_athena_workgroup_query_results_encrypt_at_rest_using_customer_managed_cmk_pass(self):
        # Arrange
        athena_workgroup: AthenaWorkgroup = create_empty_entity(AthenaWorkgroup)
        athena_workgroup.iac_state = IacState(address='address',
                                              action=IacActionType.CREATE,
                                              resource_metadata=None,
                                              is_new=False)

        context = AwsEnvironmentContext(athena_workgroups=[athena_workgroup])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
