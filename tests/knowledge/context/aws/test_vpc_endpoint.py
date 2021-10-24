from cloudrail.knowledge.context.mergeable import EntityOrigin

from cloudrail.knowledge.context.connection import ConnectionDetail, ConnectionType
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.resources.ec2.vpc_endpoint import VpcEndpointGateway, VpcEndpointInterface
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestVpcEndpoint(AwsContextTest):

    def get_component(self):
        return "vpc_endpoint"

    @context(module_path="vpc-endpoint-rtb-assignment-by-ids")
    def test_vpc_endpoint_rtb_assignment_by_ids(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.vpc_endpoints), 1)
        vpce: VpcEndpointGateway = ctx.vpc_endpoints[0]
        self.assertEqual(len(vpce.route_table_ids), 1)
        self.assertEqual(len(vpce.route_tables), 1)
        self.assertTrue(vpce.route_tables[0] in ctx.route_tables)
        if not vpce.is_managed_by_iac:
            self.assertEqual(vpce.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/vpc/home?region=us-east-1#Endpoints:vpcEndpointId=vpce-0ff0472829dbbf9e7')

    @context(module_path="vpc-endpoint-rtb-assignment-by-association")
    def test_vpc_endpoint_rtb_assignment_by_association(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.vpc_endpoints), 1)
        vpce: VpcEndpointGateway = ctx.vpc_endpoints[0]
        self.assertEqual(len(vpce.route_tables), 1)
        self.assertTrue(vpce.route_tables[0] in ctx.route_tables)

    @context(module_path="vpc-endpoint-inbound-connections")
    def test_vpc_endpoint_inbound_connections(self, ctx: AwsEnvironmentContext):
        vpce: VpcEndpointInterface = self._assert_vpc_endpoint_eni(ctx)
        self.assertEqual(len(vpce.network_resource.inbound_connections), 1)
        conn_details: ConnectionDetail = vpce.network_resource.inbound_connections[0]
        self.assertEqual(conn_details.connection_type, ConnectionType.PRIVATE)
        self.assertEqual(conn_details.target_instance.owner, ctx.ec2s[0])
        conn_details: ConnectionDetail = next((conn for conn in vpce.network_resource.outbound_connections
                                               if conn.connection_type == ConnectionType.PRIVATE), None)
        self.assertEqual(conn_details.connection_type, ConnectionType.PRIVATE)
        self.assertEqual(conn_details.target_instance.owner, ctx.ec2s[0])

    @context(module_path="vpc-endpoint-eni")
    def test_vpc_endpoint_eni(self, ctx: AwsEnvironmentContext):
        vpce: VpcEndpointInterface = self._assert_vpc_endpoint_eni(ctx)
        eni: NetworkInterface = vpce.network_resource.network_interfaces[0]
        self.assertEqual(eni.subnet, ctx.subnets[vpce.subnet_ids[0]])
        self.assertEqual(eni.security_groups[0], ctx.security_groups[vpce.security_group_ids[0]])
        self.assertEqual(eni.owner, vpce)

    def _assert_vpc_endpoint_eni(self, ctx: AwsEnvironmentContext) -> VpcEndpointInterface:
        self.assertEqual(len(ctx.vpc_endpoints), 1)
        vpce: VpcEndpointInterface = ctx.vpc_endpoints[0]
        self.assertGreater(len(ctx.vpcs.keys()), 0)
        self.assertIsNotNone(ctx.vpcs.get(vpce.vpc_id))
        self.assertEqual(vpce.region, 'us-east-1')
        self.assertEqual(vpce.account, self.DUMMY_ACCOUNT_ID)
        if vpce.iac_state:
            if vpce.origin == EntityOrigin.TERRAFORM:
                self.assertEqual(vpce.vpce_id, 'aws_vpc_endpoint.lambda-vpce.id')
            elif vpce.origin == EntityOrigin.CLOUDFORMATION:
                self.assertEqual(vpce.vpce_id, 'vpce-05ffa660132bf34c1')
        else:
            self.assertEqual(vpce.vpce_id, 'vpce-0190beec1d05f0f83')
        self.assertEqual(vpce.service_name, 'com.amazonaws.us-east-1.lambda')
        self.assertIsNotNone(vpce.policy)
        self.assertGreaterEqual(len(ctx.subnets.keys()), 1)
        self.assertEqual(len(vpce.subnet_ids), 1)
        self.assertIsNotNone(ctx.subnets[vpce.subnet_ids[0]])
        self.assertGreater(len(ctx.security_groups.keys()), 1)
        self.assertEqual(len(vpce.security_group_ids), 1)
        self.assertIsNotNone(ctx.security_groups[vpce.security_group_ids[0]])
        self.assertGreater(len(ctx.network_interfaces), 0)
        self.assertEqual(len(vpce.network_resource.network_interfaces), 1)
        return vpce

    @context(module_path="with_tags")
    def test_with_tags(self, ctx: AwsEnvironmentContext):
        vpce = next((vpce for vpce in ctx.vpc_endpoints if vpce.service_name == 'com.amazonaws.us-east-1.sns'), None)
        vpc = next((vpc for vpc in ctx.vpcs if '192.168.100.128/25' in vpc.cidr_block), None)
        self.assertIsNotNone(vpc)
        self.assertIsNotNone(vpce)
        self.assertTrue(vpc.tags)
        self.assertTrue(vpce.tags)
