from tests.knowledge.context.aws_context_test import AwsContextTest
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestSqsQueue(AwsContextTest):

    def get_component(self):
        return 'sqs_queues'

    @context(module_path="encrypted_at_rest")
    def test_encrypted_at_rest(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sqs_queues), 2)
        sqs_queue = next((sqs_queue for sqs_queue in ctx.sqs_queues if sqs_queue.queue_name == 'sqs_encrypted'), None)
        self.assertTrue(sqs_queue.encrypted_at_rest)
        self.assertTrue(sqs_queue.arn)
        self.assertFalse(sqs_queue.policy)
        if not sqs_queue.is_managed_by_iac:
            self.assertEqual(sqs_queue.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/sqs/v2/home?region=us-east-1#'
                             '/queues/https%3A%2F%2Fqueue.amazonaws.com%2F115553109071%2Fsqs_encrypted')

    @context(module_path="encrypted_at_rest_with_customer_managed_cmk", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_encrypted_at_rest_with_customer_managed_cmk(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sqs_queues), 1)
        self.assertTrue(ctx.sqs_queues[0].encrypted_at_rest)
        self.assertTrue(ctx.sqs_queues[0].arn)
        self.assertFalse(ctx.sqs_queues[0].policy)
        self.assertEqual(ctx.sqs_queues[0].queue_name, 'sqs_encrypted')
        self.assertEqual(ctx.sqs_queues[0].kms_key, 'arn:aws:kms:us-east-1:115553109071:key/ed8cfa36-e3fe-4981-a565-ed4ecd238d50')

    @context(module_path="no_encryption")
    def test_no_encryption(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.sqs_queues), 1)
        sqs_queue = ctx.sqs_queues[0]
        self.assertFalse(sqs_queue.encrypted_at_rest)
        self.assertFalse(sqs_queue.policy)
        self.assertFalse(sqs_queue.tags)

    @context(module_path="bad_policy")
    def test_bad_policy(self, ctx: AwsEnvironmentContext):
        sqs_queue = ctx.sqs_queues[0]
        self.assertEqual(sqs_queue.policy.statements[0].actions[0], 'sqs:*')
        self.assertTrue(sqs_queue.policy.queue_name)
        self.assertFalse(sqs_queue.encrypted_at_rest)
        self.assertTrue(sqs_queue.arn)
        self.assertEqual(sqs_queue.queue_name, 'cloudrail-not-secure-queue')

    @context(module_path="good_policy")
    def test_good_policy(self, ctx: AwsEnvironmentContext):
        sqs_queue = ctx.sqs_queues[0]
        self.assertEqual(sqs_queue.policy.statements[0].actions[0], 'sqs:SendMessage')
        self.assertTrue(sqs_queue.policy.queue_name)
        self.assertFalse(sqs_queue.encrypted_at_rest)
        self.assertTrue(sqs_queue.arn)
        self.assertEqual(sqs_queue.queue_name, 'cloudrail-secure-queue')

    @context(module_path="secure_policy_existing_queue", base_scanner_data_for_iac='account-data-existing-sqs-queue-secure-policy',
             test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False))
    def test_secure_policy_existing_queue(self, ctx: AwsEnvironmentContext):
        sqs_queue = ctx.sqs_queues[0]
        self.assertEqual(sqs_queue.policy.statements[0].actions[0], 'sqs:SendMessage')
        self.assertTrue(sqs_queue.policy.queue_name)
        self.assertFalse(sqs_queue.encrypted_at_rest)
        self.assertTrue(sqs_queue.arn)
        self.assertEqual(sqs_queue.queue_name, 'cloudrail-secure-queue_2')
        self.assertEqual(sqs_queue.account, '115553109071')
        self.assertEqual(sqs_queue.region, 'us-east-1')

    @context(module_path="bad_policy_policy_inside_main_resource")
    def test_bad_policy_policy_inside_main_resource(self, ctx: AwsEnvironmentContext):
        sqs_queue = ctx.sqs_queues[0]
        self.assertEqual(sqs_queue.policy.statements[0].actions[0], 'sqs:*')
        self.assertTrue(sqs_queue.policy.queue_name)
        self.assertFalse(sqs_queue.encrypted_at_rest)
        self.assertTrue(sqs_queue.arn)
        self.assertEqual(sqs_queue.queue_name, 'cloudrail-not-secure-queue')

    @context(module_path="with_tags")
    def test_with_tags(self, ctx: AwsEnvironmentContext):
        sqs = next((sqs for sqs in ctx.sqs_queues if sqs.queue_name == 'sqs_non_encrypted'), None)
        self.assertIsNotNone(sqs)
        self.assertTrue(sqs.tags)
