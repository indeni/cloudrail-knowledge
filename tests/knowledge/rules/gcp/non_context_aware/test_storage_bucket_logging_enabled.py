import unittest

from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucket
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.non_context_aware.storage_bucket_logging_enabled_rule import StorageBucketLoggingEnabledRule


class TestStorageBucketLoggingEnabled(unittest.TestCase):

    def setUp(self):
        self.rule = StorageBucketLoggingEnabledRule()

    def test_ssl_required(self):
        # Arrange
        bucket = create_empty_entity(GcpStorageBucket)
        bucket.name = 'my-bucket'
        bucket.logging_enable = True
        context = GcpEnvironmentContext(storage_buckets=AliasesDict(*[bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)

    def test_ssl_not_required(self):
        # Arrange
        bucket = create_empty_entity(GcpStorageBucket)
        bucket.name = 'my-bucket'
        bucket.logging_enable = False
        context = GcpEnvironmentContext(storage_buckets=AliasesDict(*[bucket]))
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
