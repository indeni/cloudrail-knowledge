from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import TestOptions, context


class TestEmrCluster(AwsContextTest):

    def get_component(self):
        return "emr_cluster"

    # Not running drift as were unable to create drift data.
    @context(module_path="basic_default_vpc", base_scanner_data_for_iac='account-data-emr-networking',
             test_options=TestOptions(run_drift_detection=False))
    def test_basic_default_vpc(self, ctx: AwsEnvironmentContext):
        emr = next((emr for emr in ctx.emr_clusters if emr.name == 'emr-test'), None)
        self.assertIsNotNone(emr)
        if not emr.is_managed_by_iac:
            self.assertEqual(emr.cluster_id, 'j-33G4WU1SOXIVF')
            self.assertEqual(emr.arn, 'arn:aws:elasticmapreduce:us-east-1:115553109071:cluster/j-33G4WU1SOXIVF')
            self.assertNotEqual(emr.get_all_network_configurations(), [])
            self.assertTrue(len(emr.vpc_config.security_groups_ids), 2)
            self.assertFalse(emr.vpc_config.assign_public_ip)
            self.assertTrue(len(emr.vpc_config.subnet_list_ids), 1)
            self.assertEqual(emr.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/elasticmapreduce/home?region=us-east-1#cluster-details:j-33G4WU1SOXIVF')
            self.assertTrue(len(emr.network_resource.network_interfaces) > 0)
            self.assertEqual(emr.master_sg_id, 'sg-01182e49a937822f8')
            self.assertEqual(emr.slave_sg_id, 'sg-0fb8dd6e1fb219f94')
        else:
            self.assertTrue(emr.cluster_id)
            self.assertTrue(emr.arn)
            self.assertNotEqual(emr.get_all_network_configurations(), [])
            self.assertEqual(len(emr.vpc_config.security_groups_ids), 2)
            self.assertFalse(emr.vpc_config.assign_public_ip)
            self.assertEqual(len(emr.vpc_config.subnet_list_ids), 1)
            self.assertTrue(len(emr.network_resource.network_interfaces) > 0)
            self.assertFalse(emr.master_sg_id)
            self.assertFalse(emr.slave_sg_id)

    @context(module_path="full_network_config", base_scanner_data_for_iac='account-data-emr-networking')
    def test_full_network_config(self, ctx: AwsEnvironmentContext):
        emr = next((emr for emr in ctx.emr_clusters if emr.name == 'emr-test'), None)
        self.assertIsNotNone(emr)
        self.assertTrue(emr.cluster_id)
        self.assertTrue(emr.arn)
        self.assertNotEqual(emr.get_all_network_configurations(), [])
        self.assertTrue(len(emr.vpc_config.security_groups_ids), 7)
        self.assertFalse(emr.vpc_config.assign_public_ip)
        self.assertTrue(len(emr.vpc_config.subnet_list_ids), 2)
        self.assertTrue(len(emr.network_resource.network_interfaces) > 0)
