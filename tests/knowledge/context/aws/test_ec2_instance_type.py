from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestEc2InstanceType(AwsContextTest):

    def get_component(self):
        return "ec2"

    @context(module_path="instance_type", test_options=TestOptions(tf_version='', run_latest_provider=False))
    def test_instance_type(self, ctx: AwsEnvironmentContext):
        for instance_type in ctx.ec2_instance_types:
            self.assertTrue(instance_type.instance_type)
            self.assertTrue(instance_type.ebs_info.ebs_optimized_support)
            self.assertTrue(instance_type.ebs_info.encryption_support)
