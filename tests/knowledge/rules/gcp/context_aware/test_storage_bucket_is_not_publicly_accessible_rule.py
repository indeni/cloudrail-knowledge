from unittest import TestCase

from cloudrail.dev_tools.rule_test_utils import create_empty_entity
from cloudrail.knowledge.context.aliases_dict import AliasesDict
from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.context.gcp.resources.iam.iam_access_policy import GcpIamPolicyBinding
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket import GcpStorageBucket
from cloudrail.knowledge.context.gcp.resources.storage.gcp_storage_bucket_iam_policy import GcpStorageBucketIamPolicy
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.knowledge.rules.gcp.context_aware.storage_bucket_is_not_publicly_accessible_rule import StorageBucketIsNotPubliclyAccessibleRule
from parameterized import parameterized


class TestStorageBucketIsNotPubliclyAccessibleRule(TestCase):
    def setUp(self):
        self.rule = StorageBucketIsNotPubliclyAccessibleRule()

    @parameterized.expand(
        [
            ["public_accessible", ['allAuthenticatedUsers'], True],
            ["not_public_accessible", ['user:joe@example.com'], False]
        ]
    )

    def test_storage_bucket_is_not_publicly_accessible_rule(self, unused_name: str, members: list, should_alert: bool):
        # Arrange
        storage_bucket: GcpStorageBucket = create_empty_entity(GcpStorageBucket)
        storage_bucket_iam_policy: GcpStorageBucketIamPolicy = create_empty_entity(GcpStorageBucketIamPolicy)
        iam_policy_binding: GcpIamPolicyBinding = create_empty_entity(GcpIamPolicyBinding)
        iam_policy_binding.members = members
        storage_bucket_iam_policy.bindings = [iam_policy_binding]
        storage_bucket.iam_policy = storage_bucket_iam_policy
        context = GcpEnvironmentContext(storage_buckets=AliasesDict(*[storage_bucket]),
                                        storage_bucket_iam_policies=[storage_bucket_iam_policy])
        # Act
        result = self.rule.run(context, {})
        # Assert
        if should_alert:
            self.assertEqual(RuleResultType.FAILED, result.status)
            self.assertEqual(1, len(result.issues))
        else:
            self.assertEqual(RuleResultType.SUCCESS, result.status)
            self.assertEqual(0, len(result.issues))
