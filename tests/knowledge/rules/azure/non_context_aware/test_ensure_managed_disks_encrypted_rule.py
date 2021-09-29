from unittest import TestCase

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
from cloudrail.knowledge.context.azure.resources.disk.azure_managed_disk import AzureManagedDisk
from cloudrail.knowledge.rules.azure.non_context_aware.ensure_managed_disks_encrypted_rule import EnsureManagedDisksEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType


class TestEnsureManagedDisksEncryptedRule(TestCase):

    def setUp(self):
        self.rule = EnsureManagedDisksEncryptedRule()

    def test_non_car_unattached_managed_disks_encrypted__no_encryption__fail(self):
        # Arrange
        managed_disk : AzureManagedDisk = create_empty_entity(AzureManagedDisk)
        context = AzureEnvironmentContext(managed_disks=AliasesDict(managed_disk))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_non_car_unattached_managed_disks_encrypted__encrypt_with_id__pass(self):
        # Arrange
        managed_disk : AzureManagedDisk = create_empty_entity(AzureManagedDisk)
        managed_disk.disk_encryption_set_id = 'some_id'
        context = AzureEnvironmentContext(managed_disks=AliasesDict(managed_disk))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))

    def test_non_car_unattached_managed_disks_encrypted__encrypt_with_encrypt_setting__pass(self):
        # Arrange
        managed_disk : AzureManagedDisk = create_empty_entity(AzureManagedDisk)
        managed_disk.disk_encryption_enabled = True
        context = AzureEnvironmentContext(managed_disks=AliasesDict(managed_disk))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
