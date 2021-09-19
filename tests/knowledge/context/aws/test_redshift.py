from cloudrail.knowledge.context.aws.resources.redshift.redshift import RedshiftCluster
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestRedshift(AwsContextTest):

    def get_component(self):
        return 'redshift'

    @context(module_path='defaults-only-new-account', base_scanner_data_for_iac='account-data-vpc-platform')
    def test_defaults_only_new_account(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        self.assertTrue(ctx.redshift_clusters[0].is_ec2_vpc_platform)
        self.assertFalse(ctx.redshift_clusters[0].encrypted)

    @context(module_path='defaults-only-old-account', base_scanner_data_for_iac='account-data-ec2-classic-platform')
    def test_defaults_only_old_account(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        self.assertFalse(ctx.redshift_clusters[0].is_ec2_vpc_platform)

    @context(module_path='defaults-with-public-off-new-account', base_scanner_data_for_iac='account-data-vpc-platform')
    def test_defaults_with_public_off_new_account(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        self.assertTrue(ctx.redshift_clusters[0].is_ec2_vpc_platform)

    @context(module_path='defaults-with-public-off-old-account', base_scanner_data_for_iac='account-data-ec2-classic-platform')
    def test_defaults_with_public_off_old_account(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        self.assertFalse(ctx.redshift_clusters[0].is_ec2_vpc_platform)

    @context(module_path='defaults-with-no-default-vpc', base_scanner_data_for_iac='account-data-us-east-1-has-no-default-vpc',
             test_options=TestOptions(run_cloudmapper=False))
    # No use in running cloudmapper data, as this scenario cannot exist in the live environment
    def test_defaults_with_no_default_vpc(self, ctx: AwsEnvironmentContext):
        self.assertTrue(any(isinstance(x, RedshiftCluster) and x.is_invalidated and x.name == 'redshift-defaults-only'
                            for x in ctx.invalidated_resources))

    @context(module_path="vpc-controlled-not-public")
    def test_vpc_controlled_not_public(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        redshift = ctx.redshift_clusters[0]
        self.assertTrue(redshift.is_ec2_vpc_platform)
        self.assertFalse(redshift.network_configuration.assign_public_ip)
        self.assertEqual(len(redshift.network_configuration.security_groups_ids), 1)
        self.assertEqual(len(redshift.network_configuration.subnet_list_ids), 2)
        self.assertEqual(len(redshift.network_resource.network_interfaces), 2)
        self.assertEqual(len(redshift.network_resource.public_ip_addresses), 0)

    @context(module_path="vpc-controlled-public")
    def test_vpc_controlled_public(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        redshift = ctx.redshift_clusters[0]
        self.assertTrue(redshift.is_ec2_vpc_platform)
        self.assertTrue(redshift.network_configuration.assign_public_ip)
        self.assertEqual(len(redshift.network_configuration.security_groups_ids), 1)
        self.assertEqual(len(redshift.network_configuration.subnet_list_ids), 2)
        self.assertEqual(len(redshift.network_resource.network_interfaces), 2)
        self.assertEqual(len(redshift.network_resource.public_ip_addresses), 2)

    @context(module_path="encrypted_cluster", base_scanner_data_for_iac='account-data-ec2-classic-platform')
    def test_encrypted_cluster(self, ctx: AwsEnvironmentContext):
        self.assertEqual(1, len(ctx.redshift_clusters))
        self.assertTrue(ctx.redshift_clusters[0].encrypted)
        self.assertFalse(ctx.redshift_clusters[0].tags)
        self.assertEqual(ctx.redshift_clusters[0].get_cloud_resource_url(),
                         'https://console.aws.amazon.com/redshiftv2/home?region=us-east-1#'
                         'cluster-details?cluster=cloudrail-redshift-cluster-encrypted')

    @context(module_path="encrypted_with_tags")
    def test_encrypted_with_tags(self, ctx: AwsEnvironmentContext):
        redshift = next((red for red in ctx.redshift_clusters if red.name == 'cloudrail-redshift-cluster-encrypted'), None)
        self.assertIsNotNone(redshift)
        self.assertTrue(redshift.tags)

    @context(module_path="vpc_controlled_public_with_tags")
    def test_vpc_controlled_public_with_tags(self, ctx: AwsEnvironmentContext):
        redshift_subnet = next((red for red in ctx.redshift_subnet_groups if red.name == 'nondefault'), None)
        self.assertIsNotNone(redshift_subnet)
        self.assertTrue(redshift_subnet.tags)

    @context(module_path="redshift_with_logs_enabled")
    def test_redshift_with_logs_enabled(self, ctx: AwsEnvironmentContext):
        redshift_logs = next((red for red in ctx.redshift_logs if red.cluster_identifier == 'cloudrail-redshift-cluster-logging'), None)
        self.assertIsNotNone(redshift_logs)
        self.assertTrue(redshift_logs.logging_enabled)
        self.assertTrue(redshift_logs.s3_bucket)
        self.assertIn('test-prefix', redshift_logs.s3_prefix)
        self.assertEqual(redshift_logs.get_cloud_resource_url(),
                         'https://console.aws.amazon.com/redshiftv2/home?region=us-east-1#cluster-details?'
                         'cluster=cloudrail-redshift-cluster-logging&tab=properties')
        redshift_cluster = next((red for red in ctx.redshift_clusters if red.name == 'cloudrail-redshift-cluster-logging'), None)
        self.assertIsNotNone(redshift_cluster)
        self.assertTrue(redshift_cluster.logs_config.logging_enabled)
        self.assertTrue(redshift_cluster.logs_config.s3_bucket)
        self.assertIn('test-prefix', redshift_cluster.logs_config.s3_prefix)

    @context(module_path="redshift_with_no_logs")
    def test_redshift_with_no_logs(self, ctx: AwsEnvironmentContext):
        redshift_logs = next((red for red in ctx.redshift_logs if red.cluster_identifier == 'cloudrail-redshift-cluster-logging'), None)
        self.assertIsNotNone(redshift_logs)
        self.assertFalse(redshift_logs.logging_enabled)
        self.assertIsNone(redshift_logs.s3_bucket)
        self.assertIsNone(redshift_logs.s3_prefix)
