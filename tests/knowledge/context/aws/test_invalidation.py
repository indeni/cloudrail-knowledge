from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.autoscaling.launch_template import LaunchTemplate
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestInvalidation(AwsContextTest):

    def get_component(self):
        return "invalidation"

    @context(module_path="cm_test_missing_vpc", test_options=TestOptions(run_terraform=False, run_drift_detection=False))
    def test_cm_test_missing_vpc(self, ctx: AwsEnvironmentContext):
        all_resources = ctx.get_all_mergeable_resources()
        self.assertGreater(len(ctx.invalidated_resources), 0)
        for invalidated_resource in ctx.invalidated_resources:
            self.assertIn('Resource with id: vpc-7f11dd02 was not found', invalidated_resource.invalidation)
            self.assertNotIn(invalidated_resource, all_resources)

    @context(module_path="tf_test_missing_vpc_and_sg", test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_tf_test_missing_vpc_and_sg(self, ctx: AwsEnvironmentContext):
        all_resources = ctx.get_all_mergeable_resources()
        self.assertEqual(len(ctx.invalidated_resources), 2)
        invalidated_subnet = next((subnet for subnet in ctx.invalidated_resources if isinstance(subnet, Subnet)))
        invalidated_launch_template = next((l_t for l_t in ctx.invalidated_resources if isinstance(l_t, LaunchTemplate)))

        self.assertIn('Resource with id: vpc-1234567 was not found', invalidated_subnet.invalidation)
        self.assertNotIn(invalidated_subnet, all_resources)  # Assert deletion from AliasesDict collection
        self.assertIn('Resource with id: sg-1234567 was not found', invalidated_launch_template.invalidation)
        self.assertNotIn(invalidated_launch_template, all_resources)  # Assert deletion from a list

    @context(module_path="missing_default_vpc", test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False),
             base_scanner_data_for_iac='account-data-missing-default-vpc.zip')
    def test_missing_default_vpc(self, ctx: AwsEnvironmentContext):
        # Deploying a redshift cluster without specifying a VPC results in the redshift being deployed in the default VPC.
        # However since the default VPC is missing, the redshift should be invalidated.
        redshift = next((redshift for redshift in ctx.invalidated_resources if isinstance(redshift, RedshiftCluster)), None)
        self.assertIsNotNone(redshift)
        self.assertTrue(any(x == 'Could not find default vpc in the region us-east-1 for account 111111111111' for x in redshift.invalidation))
        self.assertNotIn(redshift, ctx.redshift_clusters)
