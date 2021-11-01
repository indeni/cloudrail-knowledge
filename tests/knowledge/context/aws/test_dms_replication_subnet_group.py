from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.iac_type import IacType
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestDmsReplicationInstanceSubnetGroup(AwsContextTest):

    def get_component(self):
        return "dms_subnet_group"

    @context(module_path="public_accessed")
    def test_public_accessed(self, ctx: AwsEnvironmentContext):
        dms_subnet_group = next((dms_rep for dms_rep in ctx.dms_replication_instance_subnet_groups
                                 if dms_rep.rep_subnet_group_id == 'test-dms-replication-subnet-group-tf'), None)
        self.assertIsNotNone(dms_subnet_group)
        self.assertEqual(dms_subnet_group.get_cloud_resource_url(),
                         "https://console.aws.amazon.com/dms/v2/home?region=us-east-1#subnetGroupDetail/test-dms-replication-subnet-group-tf")
        self.assertTrue(isinstance(dms_subnet_group.subnet_ids, list))
        self.assertTrue(len(dms_subnet_group.subnet_ids), 2)
        if dms_subnet_group.is_managed_by_iac:
            if dms_subnet_group.iac_state.iac_type == IacType.TERRAFORM:
                self.assertEqual(dms_subnet_group.vpc_id, 'aws_dms_replication_subnet_group.test.vpc_id')
            elif dms_subnet_group.iac_state.iac_type == IacType.CLOUDFORMATION:
                self.assertEqual(dms_subnet_group.vpc_id, 'vpc-0611b9b243b4a5ade')
        else:
            self.assertEqual(dms_subnet_group.vpc_id, 'vpc-095cde8ba4f442498')
