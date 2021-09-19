from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from test.knowledge.context.aws_context_test import AwsContextTest
from test.knowledge.context.test_context_annotation import context, TestOptions


class TestDefaultResources(AwsContextTest):

    def get_component(self):
        return "default_resources"

    @context(module_path="security_group_already_adopted", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_security_group_already_adopted(self, ctx: AwsEnvironmentContext):
        security_group = ctx.security_groups['sg-0f5fa3490cfe7cb79']
        self.assertEqual(len(security_group.inbound_permissions), 0)
        self.assertEqual(len(security_group.outbound_permissions), 1)
        self.assertEqual(len(security_group.tags), 2)

    @context(module_path="security_group_first_adoption", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_security_group_first_adoption(self, ctx: AwsEnvironmentContext):
        security_group = ctx.security_groups['sg-0f5fa3490cfe7cb79']
        self.assertEqual(len(security_group.inbound_permissions), 0)
        self.assertEqual(len(security_group.outbound_permissions), 1)
        self.assertEqual(len(security_group.tags), 2)

    @context(module_path="security_group_without_rules", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_security_group_without_rules(self, ctx: AwsEnvironmentContext):
        security_group = ctx.security_groups['sg-0f5fa3490cfe7cb79']
        self.assertEqual(len(security_group.inbound_permissions), 0)
        self.assertEqual(len(security_group.outbound_permissions), 0)
        self.assertEqual(len(security_group.tags), 2)

    @context(module_path="route_table_already_adopted", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_route_table_already_adopted(self, ctx: AwsEnvironmentContext):
        route_table = ctx.route_tables['rtb-0a8787b494abdc57b']
        self.assertEqual(len(route_table.routes), 2)
        # Checking that the already-existing route to an ENI is deleted, and only the 'local' + tf-defined route (to IGW) are kept
        self.assertTrue(all(route.target.startswith('igw-') or route.target == 'local'  for route in route_table.routes))
        self.assertEqual(len(route_table.tags), 2)

    @context(module_path="route_table_first_adoption", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_route_table_first_adoption(self, ctx: AwsEnvironmentContext):
        route_table = ctx.route_tables['rtb-0a8787b494abdc57b']
        self.assertEqual(len(route_table.routes), 2)
        # Checking that the already-existing route to an ENI is deleted, and only the 'local' + tf-defined route (to IGW) are kept
        self.assertTrue(all(route.target.startswith('igw-') or route.target == 'local' for route in route_table.routes))
        self.assertEqual(len(route_table.tags), 2)

    @context(module_path="nacl_already_adopted", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_nacl_already_adopted(self, ctx: AwsEnvironmentContext):
        nacl = ctx.network_acls['acl-017afdbe80a556293']
        self.assertEqual(len(nacl.inbound_rules), 2)  # Should have the TF-defiined rule and the default deny-all rule with highest rule numbeer
        self.assertEqual(len(nacl.outbound_rules), 1)  # Should have only the default deny-all rule since no egress rule defined in the TF
        self.assertEqual(len(nacl.tags), 2)

    @context(module_path="nacl_first_adoption", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_nacl_first_adoption(self, ctx: AwsEnvironmentContext):
        nacl = ctx.network_acls['acl-017afdbe80a556293']
        self.assertEqual(len(nacl.inbound_rules), 2)  # Should have the TF-defiined rule and the default deny-all rule with highest rule numbeer
        self.assertEqual(len(nacl.outbound_rules), 1)  # Should have only the default deny-all rule since no egress rule defined in the TF
        self.assertEqual(len(nacl.tags), 2)

    @context(module_path="nacl_with_subnets", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_nacl_with_subnets(self, ctx: AwsEnvironmentContext):
        nacl = ctx.network_acls['acl-017afdbe80a556293']
        self.assertEqual(len(nacl.subnet_ids), 2)

    @context(module_path="subnet_first_adoption_without_map_public_ip_on_launch", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_subnet_first_adoption_without_map_public_ip_on_launch(self, ctx: AwsEnvironmentContext):
        subnet = ctx.subnets['subnet-6e81fd22']
        self.assertEqual(len(subnet.tags), 2)
        self.assertTrue(subnet.map_public_ip_on_launch)  # Should have the scanner definition

    @context(module_path="subnet_first_adoption_map_public_ip_on_launch_true", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_subnet_first_adoption_map_public_ip_on_launch_true(self, ctx: AwsEnvironmentContext):
        subnet = ctx.subnets['subnet-6e81fd22']
        self.assertEqual(len(subnet.tags), 2)
        self.assertTrue(subnet.map_public_ip_on_launch)  # Should have the terraform definition

    @context(module_path="subnet_first_adoption_map_public_ip_on_launch_false", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_subnet_first_adoption_map_public_ip_on_launch_false(self, ctx: AwsEnvironmentContext):
        subnet = ctx.subnets['subnet-6e81fd22']
        self.assertEqual(len(subnet.tags), 2)
        self.assertFalse(subnet.map_public_ip_on_launch)  # Should have the terraform definition

    @context(module_path="subnet_already_adopted_without_map_public_ip_on_launch", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_subnet_already_adopted_without_map_public_ip_on_launch(self, ctx: AwsEnvironmentContext):
        subnet = ctx.subnets['subnet-6e81fd22']
        self.assertEqual(len(subnet.tags), 2)
        self.assertTrue(subnet.map_public_ip_on_launch)  # Should have the scanner definition

    @context(module_path="subnet_already_adopted_map_public_ip_on_launch_true", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_subnet_already_adopted_map_public_ip_on_launch_true(self, ctx: AwsEnvironmentContext):
        subnet = ctx.subnets['subnet-6e81fd22']
        self.assertEqual(len(subnet.tags), 2)
        self.assertTrue(subnet.map_public_ip_on_launch)  # Should have the terraform definition

    @context(module_path="subnet_already_adopted_map_public_ip_on_launch_false", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_subnet_already_adopted_map_public_ip_on_launch_false(self, ctx: AwsEnvironmentContext):
        subnet = ctx.subnets['subnet-6e81fd22']
        self.assertEqual(len(subnet.tags), 2)
        self.assertFalse(subnet.map_public_ip_on_launch)  # Should have the terraform definition

    @context(module_path="vpc_already_adopted", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_vpc_already_adopted(self, ctx: AwsEnvironmentContext):
        vpc = ctx.vpcs['vpc-0e289f65']
        self.assertEqual(len(vpc.tags), 2)
        self.assertFalse(vpc.enable_dns_hostnames)  # Should have the terraform definition
        self.assertTrue(vpc.enable_dns_support)  # Should have the scanner definition

    @context(module_path="vpc_first_adoption", base_scanner_data_for_iac='account-data-defaults-merger',
             test_options=TestOptions(run_cloudmapper=False, run_drift_detection=False))
    def test_vpc_first_adoption(self, ctx: AwsEnvironmentContext):
        vpc = ctx.vpcs['vpc-0e289f65']
        self.assertEqual(len(vpc.tags), 2)
        self.assertFalse(vpc.enable_dns_hostnames)  # Should have the terraform definition
        self.assertTrue(vpc.enable_dns_support)  # Should have the scanner definition
