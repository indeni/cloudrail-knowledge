from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context


class TestCloudWatchLogsDestinationPolicy(AwsContextTest):

    def get_component(self):
        return "cloudwatch_logs_destinations"

    @context(module_path="not_secure_policy")
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        destination_policy = ctx.cloudwatch_logs_destination_policies[0]
        self.assertEqual(destination_policy.destination_name, 'test_destination')
        self.assertEqual(destination_policy.statements[0].effect, StatementEffect.ALLOW)
        self.assertEqual(destination_policy.statements[0].actions, ['logs:*'])
