from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestEcrRepositoryPolicy(AwsContextTest):

    def get_component(self):
        return "ecr_repositories"

    @context(module_path="non_secure_policy")
    def test_non_secure_policy(self, ctx: AwsEnvironmentContext):
        self.assertTrue(len(ctx.ecr_repositories_policy), 1)
        ecr_repo = ctx.ecr_repositories_policy[0]
        self.assertEqual(ecr_repo.repo_name, 'not_secure_ecr')
        self.assertEqual(ecr_repo.statements[0].actions, ['ecr:*'])
        self.assertEqual(ecr_repo.statements[0].effect, StatementEffect.ALLOW)
