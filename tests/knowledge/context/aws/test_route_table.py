from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestRouteTable(AwsContextTest):

    def get_component(self):
        return 'route_table'

    @context(module_path="default_route_table_defined")
    def test_default_route_table_defined(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.server_name == 'external'), None)
        route_table = next((rt for rt in ctx.route_tables if rt.vpc_id == vpc.vpc_id), None)
        subnet = next((subnet for subnet in ctx.subnets if subnet.vpc_id == vpc.vpc_id), None)
        self.assertEqual(2, len(route_table.routes))
        self.assertEqual(route_table, subnet.route_table)
        self.assertTrue(route_table.tags)
        if not route_table.is_managed_by_iac:
            self.assertEqual(route_table.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/vpc/home?region=us-east-1#RouteTables:routeTableId=rtb-033c9923642c154cf')
            self.assertEqual(subnet.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/vpc/home?region=us-east-1#SubnetDetails:subnetId=subnet-0b16dcce8147e25f8')

    @context(module_path="main_route_table_defined")
    def test_main_route_table_defined(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.server_name == 'external'), None)
        subnet = next((subnet for subnet in ctx.subnets if subnet.vpc_id == vpc.vpc_id), None)
        self.assertEqual(vpc.main_route_table, subnet.route_table)

    @context(module_path="main_and_default_route_table_not_defined")
    def test_main_and_default_route_table_not_defined(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.server_name == 'external'), None)
        subnet = next((subnet for subnet in ctx.subnets if subnet.vpc_id == vpc.vpc_id), None)
        self.assertEqual(vpc.main_route_table, subnet.route_table)
