from cloudrail.knowledge.context.gcp.gcp_environment_context import GcpEnvironmentContext
from cloudrail.knowledge.exceptions import UnknownResultOfTerraformApply
from tests.knowledge.context.gcp_context_test import GcpContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestStorageBucketIamPolicy(GcpContextTest):
    def get_component(self):
        return 'storage_bucket_iam_policy'

    @context(module_path="iam_policy")
    def test_basic_iam_policy(self, ctx: GcpEnvironmentContext):
        storage_bucket_iam_policy = next((policy for policy in ctx.storage_bucket_iam_policies
                                          if policy.bucket_name == 'dereban' and not policy.is_default), None)
        self.assertIsNotNone(storage_bucket_iam_policy)
        self.assertEqual(storage_bucket_iam_policy.bucket_name, 'dereban')
        self.assertEqual(len(storage_bucket_iam_policy.bindings), 1)
        self.assertEqual(storage_bucket_iam_policy.bindings[0].role, 'roles/storage.admin')
        self.assertEqual(storage_bucket_iam_policy.bindings[0].members, ['allAuthenticatedUsers'])

    @context(module_path="iam_policy")
    def test_iam_policy_assign_to_bucket(self, ctx: GcpEnvironmentContext):
        storage_bucket = next((bucket for bucket in ctx.storage_buckets if bucket.name == 'dereban'), None)
        self.assertIsNotNone(storage_bucket)
        self.assertTrue(storage_bucket.iam_policy)
        self.assertEqual(len(storage_bucket.iam_policy.bindings), 1)

    @context(module_path="iam_policy_binding")
    def test_iam_policy_binding(self, ctx: GcpEnvironmentContext):
        storage_bucket_iam_policy = next((policy for policy in ctx.storage_bucket_iam_policies
                                          if policy.bucket_name == 'dereban' and not policy.is_default), None)
        self.assertIsNotNone(storage_bucket_iam_policy)
        self.assertEqual(storage_bucket_iam_policy.bucket_name, 'dereban')
        self.assertEqual(len(storage_bucket_iam_policy.bindings), 5)
        binding_policy = next((binding for binding in storage_bucket_iam_policy.bindings
                               if binding.members == ['user:maksym.d@indeni.com']), None)
        self.assertEqual(binding_policy.role, 'roles/storage.admin')
        self.assertTrue(binding_policy.condition)
        self.assertEqual(binding_policy.condition.description, 'Expiring at midnight of 2021-12-31')
        self.assertEqual(binding_policy.condition.expression, 'request.time < timestamp(\"2020-01-01T00:00:00Z\")')
        self.assertEqual(binding_policy.condition.title, 'expires_after_2021_12_31')

    @context(module_path="iam_policy_binding")
    def test_iam_policy_binding_assign_to_bucket(self, ctx: GcpEnvironmentContext):
        storage_bucket = next((bucket for bucket in ctx.storage_buckets if bucket.name == 'dereban'), None)
        self.assertIsNotNone(storage_bucket)
        self.assertTrue(storage_bucket.iam_policy)
        self.assertEqual(len(storage_bucket.iam_policy.bindings), 5)

    @context(module_path="iam_policy_member")
    def test_iam_policy_member(self, ctx: GcpEnvironmentContext):
        storage_bucket_iam_policy = next((policy for policy in ctx.storage_bucket_iam_policies
                                          if policy.bucket_name == 'dereban' and not policy.is_default), None)
        self.assertIsNotNone(storage_bucket_iam_policy)
        self.assertEqual(storage_bucket_iam_policy.bucket_name, 'dereban')
        self.assertEqual(len(storage_bucket_iam_policy.bindings), 5)
        binding_policy = next((binding for binding in storage_bucket_iam_policy.bindings
                               if binding.members == ['user:maksym.d@indeni.com']), None)
        self.assertEqual(binding_policy.role, 'roles/storage.admin')
        self.assertTrue(binding_policy.condition)
        self.assertEqual(binding_policy.condition.description, 'Expiring at midnight of 2019-12-31')
        self.assertEqual(binding_policy.condition.expression, 'request.time < timestamp(\"2020-01-01T00:00:00Z\")')
        self.assertEqual(binding_policy.condition.title, 'expires_after_2019_12_31')

    @context(module_path="iam_policy_member")
    def test_iam_policy_member_assign_to_bucket(self, ctx: GcpEnvironmentContext):
        storage_bucket = next((bucket for bucket in ctx.storage_buckets if bucket.name == 'dereban'), None)
        self.assertIsNotNone(storage_bucket)
        self.assertTrue(storage_bucket.iam_policy)
        self.assertEqual(len(storage_bucket.iam_policy.bindings), 5)

    @context(module_path="unsupported_scenraio",
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False, expected_exception=UnknownResultOfTerraformApply))
    def test_iam_policy_raise_exception(self, ctx: GcpEnvironmentContext):
        pass
