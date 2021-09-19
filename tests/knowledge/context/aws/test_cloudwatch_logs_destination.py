from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestCloudWatchLogsDestination(AwsContextTest):

    def get_component(self):
        return "cloudwatch_logs_destinations"

    @context(module_path="not_secure_policy", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        destination = ctx.cloudwatch_logs_destinations[0]
        self.assertEqual(destination.name, 'test_destination')
        self.assertTrue(destination.arn)
        self.assertEqual(destination.policy.statements[0].effect, StatementEffect.ALLOW)
        self.assertEqual(destination.policy.statements[0].actions, ['logs:*'])

    @context(module_path="secure_policy_tf_address_data_resource", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_secure_policy_tf_address_data_resource(self, ctx: AwsEnvironmentContext):
        destination = ctx.cloudwatch_logs_destinations[0]
        self.assertEqual(destination.name, 'test_destination')
        self.assertTrue(destination.arn)
        if destination.policy:
            self.assertEqual(destination.policy.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(destination.policy.statements[0].actions, ['logs:PutSubscriptionFilter'])
