from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.iam.policy_statement import StatementEffect

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestGlueDataCatalogPolicy(AwsContextTest):

    def get_component(self):
        return "glue_data_catalog/resource_policy"

    # # Not testing TF, as it has no policy_hash value like CM.
    @context(module_path="not_secure_policy", test_options=TestOptions(run_terraform=False, run_drift_detection=False))
    def test_not_secure_policy(self, ctx: AwsEnvironmentContext):
        gdc_policy = next((gdc_policy for gdc_policy in ctx.glue_data_catalog_policy if \
                           gdc_policy.statements[0].actions == ['glue:*']), None)
        self.assertIsNotNone(gdc_policy)
        self.assertEqual(gdc_policy.statements[0].effect, StatementEffect.ALLOW)

    @context(module_path="secure_policy", test_options=TestOptions(tf_version='>3.13.0'))
    def test_secure_policy(self, ctx: AwsEnvironmentContext):
        gdc_policy = next((gdc_policy for gdc_policy in ctx.glue_data_catalog_policy if \
                           gdc_policy.statements[0].actions == ['glue:CreateTable']), None)
        self.assertIsNotNone(gdc_policy)
        self.assertEqual(gdc_policy.statements[0].effect, StatementEffect.ALLOW)
