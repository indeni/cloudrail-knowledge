from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestDmsReplicationInstance(AwsContextTest):

    def get_component(self):
        return "dms"

    @context(module_path="public_accessed")
    def test_public_accessed(self, ctx: AwsEnvironmentContext):
        dms_rep = next((dms_rep for dms_rep in ctx.dms_replication_instances
                        if dms_rep.name == 'test-dms-replication-instance-tf'), None)
        self.assertIsNotNone(dms_rep)
        self.assertEqual(dms_rep.get_cloud_resource_url(),
                         "https://console.aws.amazon.com/dms/v2/home?region=us-east-1#replicationInstanceDetails/test-dms-replication-instance-tf")
        self.assertTrue(dms_rep.arn)
        self.assertTrue(dms_rep.publicly_accessible)
        self.assertEqual(dms_rep.rep_instance_subnet_group_id, 'test-dms-replication-subnet-group-tf')
        self.assertTrue(isinstance(dms_rep.security_group_ids, list))
        self.assertEqual(len(dms_rep.security_group_ids), 1)
        self.assertTrue(isinstance(dms_rep.subnet_ids, list))
        self.assertEqual(len(dms_rep.subnet_ids), 2)
        self.assertFalse(dms_rep.is_in_default_vpc)

    @context(module_path="dms_public_access_tf_using_id")
    def test_dms_public_access_tf_using_id(self, ctx: AwsEnvironmentContext):
        dms_rep = next((dms_rep for dms_rep in ctx.dms_replication_instances
                        if dms_rep.name == 'test-dms-replication-instance-tf'), None)
        self.assertIsNotNone(dms_rep)
        self.assertTrue(dms_rep.publicly_accessible)
        self.assertTrue(dms_rep.rep_instance_subnet_group_id in ('test-dms-replication-subnet-group-tf', 'aws_dms_replication_subnet_group.test.id'))
        self.assertTrue(isinstance(dms_rep.security_group_ids, list))
        self.assertEqual(len(dms_rep.security_group_ids), 1)
        self.assertTrue(isinstance(dms_rep.subnet_ids, list))
        self.assertEqual(len(dms_rep.subnet_ids), 2)
        self.assertFalse(dms_rep.is_in_default_vpc)

    @context(module_path="no_public_access", base_scanner_data_for_iac='account-data-dms-instance-networking.zip')
    def test_no_public_access(self, ctx: AwsEnvironmentContext):
        dms_rep = next((dms_rep for dms_rep in ctx.dms_replication_instances
                        if dms_rep.name == 'test-dms-replication-instance-tf'), None)
        self.assertIsNotNone(dms_rep)
        self.assertTrue(dms_rep.arn)
        self.assertFalse(dms_rep.publicly_accessible)
        self.assertEqual(dms_rep.rep_instance_subnet_group_id, 'default')
        self.assertTrue(isinstance(dms_rep.security_group_ids, list))
        self.assertEqual(len(dms_rep.security_group_ids), 1)
        self.assertTrue(isinstance(dms_rep.subnet_ids, list))
        self.assertEqual(len(dms_rep.subnet_ids), 6)

    @context(module_path="default_vpc_public_access", base_scanner_data_for_iac='account-data-dms-instance-networking-public.zip')
    def test_default_vpc_public_access(self, ctx: AwsEnvironmentContext):
        dms_rep = next((dms_rep for dms_rep in ctx.dms_replication_instances
                        if dms_rep.name == 'test-dms-replication-instance-tf'), None)
        self.assertIsNotNone(dms_rep)
        self.assertTrue(dms_rep.arn)
        self.assertTrue(dms_rep.publicly_accessible)
        self.assertEqual(dms_rep.rep_instance_subnet_group_id, 'default')
        self.assertTrue(dms_rep.is_in_default_vpc)
        self.assertTrue(isinstance(dms_rep.security_group_ids, list))
        self.assertEqual(len(dms_rep.security_group_ids), 1)
        self.assertTrue(isinstance(dms_rep.subnet_ids, list))
        self.assertEqual(len(dms_rep.subnet_ids), 6)
