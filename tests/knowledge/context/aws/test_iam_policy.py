from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestIamRole(AwsContextTest):

    def get_component(self):
        return "iam/iam_policy"

    @context(module_path="iam_multiple_issues", test_options=TestOptions(run_cloudmapper=False))
    def test_iam_access_analyzer_validation_multiple_issues(self, ctx: AwsEnvironmentContext):
        for policy in ctx.role_inline_policies:
            if policy.iac_state.address == 'aws_iam_role_policy.allow-policy-1':
                self.assertEqual(1, len(policy.access_analyzer_findings))
                self.assertEqual('ERROR', policy.access_analyzer_findings[0]['findingType'])
                self.assertIsNotNone(policy.access_analyzer_findings[0].get('learnMoreLink'))
                self.assertIsNotNone(policy.access_analyzer_findings[0].get('findingDetails'))
            elif policy.iac_state.address == 'aws_iam_role_policy.allow-policy-2':
                self.assertEqual(2, len(policy.access_analyzer_findings))
                self.assertEqual('ERROR', policy.access_analyzer_findings[0]['findingType'])
                self.assertEqual('ERROR', policy.access_analyzer_findings[1]['findingType'])
            else:
                self.fail(f'unknown policy {policy.iac_state.address}')

    @context(module_path="iam_security_issues", test_options=TestOptions(run_cloudmapper=False))
    def test_iam_access_analyzer_validation_security_issues(self, ctx: AwsEnvironmentContext):
        for policy in ctx.role_inline_policies:
            if policy.iac_state.address == 'aws_iam_role_policy.allow-policy-1':
                self.assertEqual(1, len(policy.access_analyzer_findings))
                self.assertEqual('SECURITY_WARNING', policy.access_analyzer_findings[0]['findingType'])
                self.assertIsNotNone(policy.access_analyzer_findings[0].get('learnMoreLink'))
                self.assertIsNotNone(policy.access_analyzer_findings[0].get('findingDetails'))
            elif policy.iac_state.address == 'aws_iam_role_policy.allow-policy-2':
                self.assertEqual(0, len(policy.access_analyzer_findings))
            else:
                self.fail(f'unknown policy {policy.iac_state.address}')

        assume_role_policy = ctx.assume_role_policies[0]
        self.assertEqual(1, len(assume_role_policy.access_analyzer_findings))
        self.assertEqual('SUGGESTION', assume_role_policy.access_analyzer_findings[0]['findingType'])
