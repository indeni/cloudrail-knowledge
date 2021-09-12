import unittest

from parameterized import parameterized

from cloudrail.dev_tools.rule_test_utils import create_empty_entity, add_terraform_state
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.aws.resources.fsx.fsx_windows_file_system import FsxWindowsFileSystem
from cloudrail.knowledge.context.aws.resources.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest \
    .fsx_windows_file_system_encrypted_at_rest_with_customer_managed_cmk_rule import \
    FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestFsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule(unittest.TestCase):
    def setUp(self):
        self.rule = FsxWindowsFileSystemEncryptedAtRestWithCustomerManagedCmkRule()

    @parameterized.expand(
        [
            ['No KMS Key, Existing FSx', None, False, False],
            ['No KMS Key, New FSx', None, True, True],
            ['With AWS managed key, Existing FSx', KmsKey('', '', KeyManager.AWS, '', ''), False, False],
            ['With AWS managed key, New FSx', KmsKey('', '', KeyManager.AWS, '', ''), True, True],
            ['With Customer managed key, Existing FSx', KmsKey('', '', KeyManager.CUSTOMER, '', ''), False, False],
            ['With Customer managed key, New FSx', KmsKey('', '', KeyManager.CUSTOMER, '', ''), True, False],
        ]
    )
    def test_kms(self, unused_name: str, kms_key: KmsKey, is_new_fsx: bool, should_alert):
        # Arrange
        fsx_windows_file_system = create_empty_entity(FsxWindowsFileSystem)
        fsx_windows_file_system.kms_data = kms_key
        add_terraform_state(fsx_windows_file_system, 'friendly_name', is_new_fsx)

        context = AwsEnvironmentContext(fsx_windows_file_systems=AliasesDict(fsx_windows_file_system))
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
