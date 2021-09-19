from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestKmsKeyPolicy(AwsContextTest):

    def get_component(self):
        return "kms_keys"

    @context(module_path="kms_key_secure_policy")
    def test_kms_key_secure_policy(self, ctx: AwsEnvironmentContext):
        for kms_key_policy in ctx.kms_keys_policies:
            self.assertTrue(kms_key_policy.key_id)
            self.assertTrue(any('kms:' in action for item in kms_key_policy.statements for action in item.actions))

    @context(module_path="kms_customer_managed")
    def test_kms_customer_managed(self, ctx: AwsEnvironmentContext):
        for kms_key_policy in ctx.kms_keys_policies:
            self.assertTrue(kms_key_policy.key_id)
            self.assertEqual(kms_key_policy.statements[0].actions, ['kms:*'])
