import unittest

from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.kms.kms_key_manager import KeyManager
from cloudrail.knowledge.context.aws.resources.rds.rds_instance import RdsInstance

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestRds(AwsContextTest):

    def get_component(self):
        return 'rds'

    @context(module_path="individual-instance/defaults-only")
    def test_individual_defaults_only(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_instances), 1)
        rds_instance = ctx.rds_instances[0]
        db_subnet_group_name = ctx.rds_instances[0].db_subnet_group_name
        self.assertTrue(db_subnet_group_name is None or db_subnet_group_name == 'default')
        self.assertTrue(rds_instance.network_resource.vpc.is_default)
        self.assertFalse(rds_instance.encrypted_at_rest)
        self.assertEqual(rds_instance.backup_retention_period, 0)
        self.assertIsNone(rds_instance.db_cluster_id)
        if rds_instance.is_managed_by_iac:
            self.assertIsNone(rds_instance.instance_id)
        else:
            self.assertTrue(rds_instance.instance_id)
            self.assertEqual(rds_instance.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=terraform-20201005043031298500000001;is-cluster=false')

    @context(module_path="individual-instance/defaults-with-public-on")
    def test_individual_defaults_with_public_on(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_instances), 1)
        db_subnet_group_name = ctx.rds_instances[0].db_subnet_group_name
        self.assertTrue(db_subnet_group_name is None or db_subnet_group_name == 'default')
        self.assertTrue(ctx.rds_instances[0].network_resource.vpc.is_default)

    @context(module_path="individual-instance/vpc-controlled-not-public")
    def test_individual_vpc_controlled_not_public(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_instances), 1)
        self.assertFalse(ctx.rds_instances[0].is_in_default_vpc)
        self.assertEqual(ctx.rds_instances[0].db_subnet_group_name, 'nondefault')
        self.assertEqual(ctx.rds_instances[0].port, 3306)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.network_interfaces), 2)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.subnets), 2)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.public_ip_addresses), 0)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.security_groups), 1)

    @context(module_path="individual-instance/vpc-controlled-public")
    def test_individual_vpc_controlled_public(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_instances), 1)
        self.assertFalse(ctx.rds_instances[0].is_in_default_vpc)
        self.assertEqual(ctx.rds_instances[0].db_subnet_group_name, 'nondefault')
        self.assertEqual(ctx.rds_instances[0].port, 3306)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.network_interfaces), 2)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.subnets), 2)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.public_ip_addresses), 2)
        self.assertEqual(len(ctx.rds_instances[0].network_resource.security_groups), 1)

    @context(module_path="individual-instance/encrypted-at-rest-enabled")
    def test_individual_encrypted_at_rest_enabled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_instances), 1)
        db_subnet_group_name = ctx.rds_instances[0].db_subnet_group_name
        self.assertTrue(db_subnet_group_name is None or db_subnet_group_name == 'default')
        self.assertTrue(ctx.rds_instances[0].network_resource.vpc.is_default)
        self.assertTrue(ctx.rds_instances[0].encrypted_at_rest)

    @context(module_path="aurora/defaults-only")
    def test_aurora_defaults_only(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_clusters), 1)
        db_subnet_group_name = ctx.rds_clusters[0].db_subnet_group_name
        self.assertTrue(db_subnet_group_name is None or db_subnet_group_name == 'default')
        self.assertFalse(ctx.rds_clusters[0].encrypted_at_rest)
        self.assertEqual(ctx.rds_clusters[0].backup_retention_period, 1)

    @context(module_path="aurora/vpc-controlled")
    def test_aurora_vpc_controlled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_clusters), 1)
        rds_cluster = ctx.rds_clusters[0]
        self.assertFalse(rds_cluster.is_in_default_vpc)
        self.assertEqual(rds_cluster.port, 3306)
        if not rds_cluster.is_managed_by_iac:
            self.assertEqual(rds_cluster.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=tf-20201005042631310600000002;is-cluster=true')

    @context(module_path="aurora/cluster-with-instances")
    def test_aurora_cluster_with_instances(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_clusters), 1)
        self.assertEqual(len(ctx.rds_instances), 2)
        self.assertFalse(ctx.rds_clusters[0].is_in_default_vpc)
        self.assertEqual(ctx.rds_clusters[0].port, 3306)
        self.assertEqual(len(ctx.rds_clusters[0].cluster_instances), 2)
        for cluster in ctx.rds_clusters:
            self.assertFalse(cluster.tags)
        for instance in ctx.rds_instances:
            self.assertFalse(instance.tags)
            self.assertFalse(instance.performance_insights_enabled)
            self.assertFalse(instance.performance_insights_kms_key)

    @context(module_path="aurora/encrypted-at-rest-enabled")
    def test_aurora_encrypted_at_rest_enabled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_clusters), 1)
        db_subnet_group_name = ctx.rds_clusters[0].db_subnet_group_name
        self.assertTrue(db_subnet_group_name is None or db_subnet_group_name == 'default')
        self.assertTrue(ctx.rds_clusters[0].encrypted_at_rest)

    @context(module_path="aurora/global_cluster_encrypted_at_rest_enabled")
    def test_aurora_global_cluster_encrypted_at_rest_enabled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_global_clusters), 1)
        self.assertTrue(ctx.rds_global_clusters[0].encrypted_at_rest)

    @context(module_path="aurora/global_cluster_encrypted_at_rest_disabled")
    def test_aurora_global_cluster_encrypted_at_rest_disabled(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_global_clusters), 1)
        self.assertFalse(ctx.rds_global_clusters[0].encrypted_at_rest)

    @context(module_path="aurora/global_cluster_encrypted_at_rest_disabled_with_source_db_not_encrypted")
    def test_aurora_global_cluster_encrypted_at_rest_disabled_with_source_db_not_encrypted(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_global_clusters), 1)
        self.assertFalse(ctx.rds_global_clusters[0].encrypted_at_rest)

    @unittest.skip('Needs to be modified by jorge')
    @context(module_path="aurora/global_cluster_encrypted_at_rest_disabled_with_source_db_encrypted", \
             test_options=TestOptions(tf_version='v3.24.1', run_cloudmapper=False))
    def test_aurora_global_cluster_encrypted_at_rest_disabled_with_source_db_encrypted(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_global_clusters), 1)
        self.assertNotEqual(ctx.rds_global_clusters[0].encrypted_at_rest, False)

    @context(module_path='individual-instance/defaults-only-no-default-vpc', base_scanner_data_for_iac='account-data-us-east-1-has-no-default-vpc',
             test_options=TestOptions(run_cloudmapper=False))
    # No use in running cloudmapper data, as this scenario cannot exist in the live environment
    def test_defaults_only_no_default_vpc(self, ctx: AwsEnvironmentContext):
        self.assertTrue(any(isinstance(x, RdsInstance) and x.is_invalidated and x.name == 'aws_db_instance.test.identifier'
                            for x in ctx.invalidated_resources))

    @context(module_path="aurora/rds_cluster_instance_encrypted_with_customer_managed_cmk_creating_key", test_options=TestOptions(run_terraform=False, run_drift_detection=False))
    def test_rds_cluster_instance_encrypted_with_customer_managed_cmk_creating_key(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_instances), 2)
        for rds_instance in ctx.rds_instances:
            self.assertTrue(rds_instance.performance_insights_kms_key)
            self.assertTrue(rds_instance.performance_insights_kms_data.key_manager)

    @context(module_path='aurora/cluster_with_instances_and_tags')
    def test_aurora_cluster_with_instances_and_tags(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.rds_clusters), 1)
        for cluster in ctx.rds_clusters:
            self.assertTrue(cluster.tags)
        instance = next((instance for instance in ctx.rds_instances if instance.db_cluster_id in ['tf-20210303135954913600000002', 'aws_rds_cluster.test.id']), None)
        self.assertTrue(instance.tags)
        self.assertIsNone(instance.instance_id)
        if not instance.is_managed_by_iac:
            self.assertEqual(instance.get_cloud_resource_url(),
                                'https://console.aws.amazon.com/rds/home?region=us-east-1#database:id=tf-20210303135954913600000002;is-cluster=true')

    @context(module_path="aurora/rds_cluster_instance_insights_encrypted_with_aws_managed_cmk_by_key_arn",
             base_scanner_data_for_iac='account-data-rds-existing-keys')
    def test_rds_cluster_instance_insights_encrypted_with_aws_managed_cmk_by_key_arn(self, ctx: AwsEnvironmentContext):
        rds_instance = next((rds_instance for rds_instance in ctx.rds_instances if rds_instance.name == 'aurora-cluster-demo-1'), None)
        self.assertIsNotNone(rds_instance)
        self.assertTrue(rds_instance.performance_insights_kms_key)
        self.assertTrue(rds_instance.performance_insights_kms_data.key_manager, KeyManager.AWS)
        self.assertTrue(rds_instance.performance_insights_enabled)

    @context(module_path="cluster_and_instance_with_iam_auth_enabled")
    def test_cluster_and_instance_with_iam_auth_enabled(self, ctx: AwsEnvironmentContext):
        rds_instance = next((rds_instance for rds_instance in ctx.rds_instances
                             if rds_instance.name == 'terraform-20210531150906114600000001'
                             or rds_instance.name == 'aws_db_instance.test.identifier'), None)
        self.assertIsNotNone(rds_instance)
        self.assertEqual(rds_instance.engine_type, 'mysql')
        self.assertIn('5.7', rds_instance.engine_version)
        self.assertTrue(rds_instance.iam_database_authentication_enabled)
        rds_cluster = next((rds_cluster for rds_cluster in ctx.rds_clusters
                            if rds_cluster.cluster_id == 'cloudrail-test-auth'
                            or rds_cluster.cluster_id == 'aws_rds_cluster.default.id'), None)
        self.assertIsNotNone(rds_cluster)
        self.assertEqual(rds_cluster.engine_type, 'aurora-mysql')
        self.assertEqual(rds_cluster.engine_version, '5.7.mysql_aurora.2.03.2')
        self.assertTrue(rds_cluster.iam_database_authentication_enabled)

    @context(module_path="cluster_and_instance_without_iam_auth")
    def test_cluster_and_instance_without_iam_auth(self, ctx: AwsEnvironmentContext):
        rds_instance = next((rds_instance for rds_instance in ctx.rds_instances
                             if 'terraform-' in rds_instance.name
                             or rds_instance.name == 'aws_db_instance.test.identifier'), None)
        self.assertIsNotNone(rds_instance)
        self.assertEqual(rds_instance.engine_type, 'mysql')
        self.assertIn('5.7', rds_instance.engine_version)
        self.assertFalse(rds_instance.iam_database_authentication_enabled)
        self.assertFalse(rds_instance.cloudwatch_logs_exports)
        rds_cluster = next((rds_cluster for rds_cluster in ctx.rds_clusters
                            if rds_cluster.cluster_id == 'cloudrail-test-auth'
                            or rds_cluster.cluster_id == 'aws_rds_cluster.default.id'), None)
        self.assertIsNotNone(rds_cluster)
        self.assertEqual(rds_cluster.engine_type, 'aurora-mysql')
        self.assertEqual(rds_cluster.engine_version, '5.7.mysql_aurora.2.03.2')
        self.assertFalse(rds_cluster.iam_database_authentication_enabled)
        self.assertFalse(rds_cluster.cloudwatch_logs_exports)

    @context(module_path="cluster_and_instance_with_logging_enabled")
    def test_cluster_and_instance_with_logging_enabled(self, ctx: AwsEnvironmentContext):
        rds_instance = next((rds_instance for rds_instance in ctx.rds_instances
                             if 'terraform-' in rds_instance.name
                             or rds_instance.name == 'aws_db_instance.test.identifier'), None)
        self.assertIsNotNone(rds_instance)
        self.assertTrue(rds_instance.cloudwatch_logs_exports)
        self.assertTrue(len(rds_instance.cloudwatch_logs_exports) > 0)
        rds_cluster = next((rds_cluster for rds_cluster in ctx.rds_clusters
                            if rds_cluster.cluster_id == 'cloudrail-test-auth'
                            or rds_cluster.cluster_id == 'aws_rds_cluster.default.id'), None)
        self.assertIsNotNone(rds_cluster)
        self.assertTrue(rds_cluster.cloudwatch_logs_exports)
        self.assertTrue(len(rds_cluster.cloudwatch_logs_exports) > 0)
