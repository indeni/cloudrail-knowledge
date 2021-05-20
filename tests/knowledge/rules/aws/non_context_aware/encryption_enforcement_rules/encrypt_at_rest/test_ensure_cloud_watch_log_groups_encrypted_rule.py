
import unittest

from cloudrail.knowledge.context.aws.cloudwatch.cloud_watch_log_group import CloudWatchLogGroup
from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_cloud_watch_log_groups_encrypted_rule import \
    EnsureCloudWatchLogGroupsEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureCloudWatchLogGroupsEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureCloudWatchLogGroupsEncryptedRule()

    def test_not_car_cloudwatch_log_group_encrypted_at_rest_using_kms_cmk__kms_encryption_missing__fail(self):
        # Arrange
        cloud_watch_log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        terraform_state = create_empty_entity(TerraformState)
        cloud_watch_log_group.terraform_state = terraform_state
        cloud_watch_log_group.terraform_state.is_new = True

        context = EnvironmentContext(cloud_watch_log_groups=[cloud_watch_log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_cloudwatch_log_group_encrypted_at_rest_using_kms_cmk__kms_key_manager_is_aws__fail(self):
        # Arrange
        cloud_watch_log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        terraform_state = create_empty_entity(TerraformState)
        cloud_watch_log_group.terraform_state = terraform_state
        cloud_watch_log_group.terraform_state.is_new = True
        cloud_watch_log_group.kms_encryption = 'kms_encryption'
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.AWS
        cloud_watch_log_group.kms_data = kms_key

        context = EnvironmentContext(cloud_watch_log_groups=[cloud_watch_log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_cloudwatch_log_group_encrypted_at_rest_using_kms_cmk_pass(self):
        # Arrange
        cloud_watch_log_group: CloudWatchLogGroup = create_empty_entity(CloudWatchLogGroup)
        terraform_state = create_empty_entity(TerraformState)
        cloud_watch_log_group.terraform_state = terraform_state
        cloud_watch_log_group.terraform_state.is_new = True
        cloud_watch_log_group.kms_encryption = 'kms_encryption'
        kms_key: KmsKey = create_empty_entity(KmsKey)
        kms_key.key_manager = KeyManager.CUSTOMER
        cloud_watch_log_group.kms_data = kms_key

        context = EnvironmentContext(cloud_watch_log_groups=[cloud_watch_log_group])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
