from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.subnet import Subnet
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestCloudformationSpecialScenarios(AwsContextTest):

    def get_component(self):
        return "cloudformation_special_scenarios"

    @context(module_path="get_ref_func_without_cloud_env",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_get_ref_func_without_cloud_env(self, ctx: AwsEnvironmentContext):
        # validate getting subnet by logical id
        subnet: Subnet = ctx.subnets.get('myExistingSubnet')
        self.assertIsNotNone(subnet)

    @context(module_path="get_ref_func",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_get_ref_func(self, ctx: AwsEnvironmentContext):
        # validate getting subnet by physical id
        subnet: Subnet = ctx.subnets.get('subnet-085df35eb16f98696')
        self.assertIsNotNone(subnet)
        # validate subnet vpc id assignment by Ref function
        self.assertIsNotNone(ctx.vpcs.get(subnet.vpc_id))

    @context(module_path="ref_func_default_template_parameter",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False,
                                      cfn_template_params={'default_az': 'us-east-1b'}))
    def test_ref_func_with_template_parameter(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myExistingSubnet')
        self.assertIsNotNone(subnet)
        # validate availability zone value of template param set by non default value
        self.assertEqual(subnet.availability_zone, 'us-east-1b')

    @context(module_path="ref_func_default_template_parameter",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_ref_func_default_template_parameter(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myExistingSubnet')
        self.assertIsNotNone(subnet)
        # validate availability zone value of template param set by default value
        self.assertEqual(subnet.availability_zone, 'us-east-1a')

    @context(module_path="get_att_func",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_get_att_func(self, ctx: AwsEnvironmentContext):
        # validate getting vpc by physical id
        vpc: Vpc = ctx.vpcs.get('vpc-000a7e8b1ce43cb61')
        self.assertIsNotNone(vpc)
        self.assertIsNotNone(vpc.is_managed_by_iac)
        self.assertIsNotNone(vpc.default_nacl.network_acl_id)

        subnet = ctx.subnets.get('subnet-085df35eb16f98696')
        self.assertIsNotNone(subnet)
        self.assertEqual(subnet.cidr_block, vpc.cidr_block[0])
        # validate subnet vpc id assignment by GetAtt function
        subnet = ctx.subnets.get('myNewSubnet')
        self.assertIsNotNone(subnet)
        self.assertEqual(subnet.availability_zone, vpc.vpc_id)  # az property init with vpc id only for testing purposes

    @context(module_path="get_az_func",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_get_azs_and_select_functions(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myNewSubnet')
        self.assertIsNotNone(subnet)
        # validate availability zone value from GetAzs (without pseudo param) and select functions
        self.assertEqual(subnet.availability_zone, 'us-east-1b')

    @context(module_path="get_az_with_pseudo_parameter",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_get_az_with_pseudo_parameter(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myNewSubnet')
        self.assertIsNotNone(subnet)
        # validate availability zone value from GetAzs (with pseudo param) and select functions
        self.assertEqual(subnet.availability_zone, 'us-east-1b')

    @context(module_path="join_func",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_join_func(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myNewSubnet2')
        self.assertIsNotNone(subnet)
        # validate tag value created by Join function
        self.assertEqual(subnet.tags.get('name'), 'arn:aws:ec2:us-east-1:111111111111:subnet/myNewSubnet2')

    @context(module_path="split_and_sub_functions",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_split_and_sub_functions(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myNewSubnet2')
        self.assertIsNotNone(subnet)
        # validate cidr block value created by Sub function with key/value mapping
        self.assertEqual(subnet.cidr_block, '172.16.0.0/16')

        subnet: Subnet = ctx.subnets.get('myNewSubnet')
        self.assertIsNotNone(subnet)
        # validate cidr block value created by Sub function without key/value mapping
        self.assertEqual(subnet.cidr_block, '172.16.0.0/16')

    @context(module_path="find_in_map_func",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_find_in_map_func(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myNewSubnet')
        self.assertIsNotNone(subnet)
        # validate az value from regions mapping with pseudo param
        self.assertEqual(subnet.availability_zone, 'us-east-1f')

    @context(module_path="conditions",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_conditions(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myExistingSubnet')
        self.assertIsNotNone(subnet)
        # validate and condition
        self.assertFalse(subnet.map_public_ip_on_launch)

    @context(module_path="remove_resource_by_condition",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_remove_resource_by_condition(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('DeletedSubnet')
        # resource removed by false condition
        self.assertIsNone(subnet)

    @context(module_path="un_removed_resource_by_condition",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_un_removed_resource_by_condition(self, ctx: AwsEnvironmentContext):
        subnet: Subnet = ctx.subnets.get('myNewSubnet3')
        #  un remove resource of true condition
        self.assertIsNotNone(subnet)

    @context(module_path="cfn_resources_merge",
             test_options=TestOptions(run_cloudmapper=False, run_terraform=False, run_drift_detection=False))
    def test_cfn_resources_merge(self, ctx: AwsEnvironmentContext):
        vpc: Vpc = ctx.vpcs.get('vpc-000a7e8b1ce43cb61')
        self.assertIsNotNone(vpc)
        # validate vpc merge with CM and CFN context
        self.assertEqual(len(ctx.vpcs), len(vpc.aliases))

        subnet = ctx.subnets.get('subnet-085df35eb16f98696')
        self.assertIsNotNone(subnet)
        # validate subnet merge with CM and CFN context
        self.assertEqual(len(ctx.subnets), len(ctx.subnets) * len(subnet.aliases))
