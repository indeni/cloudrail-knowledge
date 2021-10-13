from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestEc2InstanceType(AwsContextTest):

    def get_component(self):
        return "ec2"

    # Not running drift as unable to create drift data - no TF template for this test
    @context(module_path="instance_type", test_options=TestOptions(run_drift_detection=False, run_terraform=False))
    def test_instance_type(self, ctx: AwsEnvironmentContext):
        for instance_type in ctx.ec2_instance_types:
            self.assertTrue(instance_type.instance_type)
            self.assertTrue(instance_type.ebs_info.ebs_optimized_support)
            self.assertTrue(instance_type.ebs_info.encryption_support)
