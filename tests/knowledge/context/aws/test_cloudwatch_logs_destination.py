from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestCloudWatchLogsDestination(AwsContextTest):

    def get_component(self):
        return "cloudwatch_logs_destinations"

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        destination = ctx.cloudwatch_logs_destinations[0]
        self.assertEqual(destination.name, 'test_destination')
        self.assertTrue(destination.arn)
        self.assertEqual(destination.resource_based_policy.statements[0].effect, StatementEffect.ALLOW)
        self.assertEqual(destination.resource_based_policy.statements[0].actions, ['logs:*'])

    @context(module_path="secure_policy_tf_address_data_resource")
    def test_secure_policy_tf_address_data_resource(self, ctx: AwsEnvironmentContext):
        destination = ctx.cloudwatch_logs_destinations[0]
        self.assertEqual(destination.name, 'test_destination')
        self.assertTrue(destination.arn)
        if destination.resource_based_policy:
            self.assertEqual(destination.resource_based_policy.statements[0].effect, StatementEffect.ALLOW)
            self.assertEqual(destination.resource_based_policy.statements[0].actions, ['logs:PutSubscriptionFilter'])
