from cloudrail.knowledge.context.aws.resources.ec2.nat_gateways import NatGateways
from cloudrail.knowledge.context.aws.resources.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestNatGateways(AwsContextTest):

    def get_component(self):
        return "nat_gw"

    @context(module_path="private-subnet-with-nat-gw-v1")
    def test_private_subnet_with_nat_gw(self, ctx: AwsEnvironmentContext):
        self.assertEqual(len(ctx.nat_gateway_list), 1)
        nat_gw: NatGateways = ctx.nat_gateway_list[0]
        self.assertTrue(nat_gw.tags)
        self.assertEqual(len(nat_gw.network_resource.subnets), 1)
        self.assertEqual(nat_gw.network_resource.subnets[0].subnet_id, nat_gw.subnet_id)
        self.assertEqual(len(nat_gw.network_resource.network_interfaces), 1)
        eni: NetworkInterface = nat_gw.network_resource.network_interfaces[0]
        self.assertEqual(eni.public_ip_address, nat_gw.public_ip)
        self.assertTrue(nat_gw.private_ip in eni.private_ip_addresses)
        if nat_gw.iac_state and nat_gw.origin == 'cloudformation':
            self.assertEqual(nat_gw.nat_gateway_id, 'nat-01ed6eef0ef5e89ec')
            self.assertEqual(nat_gw.allocation_id, 'eipalloc-059ba3d4437f7bcd1')
            self.assertEqual(nat_gw.subnet_id, 'subnet-09aa90b274b6ce284')
            self.assertEqual(nat_gw.eni_id, 'eni-0272293acd07c4dfd')
            self.assertEqual(nat_gw.private_ip, '192.168.100.12')
            self.assertEqual(nat_gw.public_ip, '34.192.141.96')
        elif nat_gw.iac_state:
            self.assertEqual(nat_gw.nat_gateway_id, 'aws_nat_gateway.private-subnet-nat-gw.id')
            self.assertEqual(nat_gw.allocation_id, 'aws_eip.allocate-ip-to-nat-gw.id')
            self.assertEqual(nat_gw.subnet_id, 'aws_subnet.public-subnet.id')
            self.assertEqual(nat_gw.eni_id, 'aws_nat_gateway.private-subnet-nat-gw.network_interface_id')
            self.assertEqual(nat_gw.private_ip, 'aws_nat_gateway.private-subnet-nat-gw.private_ip')
            self.assertEqual(nat_gw.public_ip, 'aws_nat_gateway.private-subnet-nat-gw.public_ip')
        else:
            self.assertEqual(nat_gw.nat_gateway_id, 'nat-0b8341023f3285b54')
            self.assertEqual(nat_gw.allocation_id, 'eipalloc-028263a579b6460a2')
            self.assertEqual(nat_gw.subnet_id, 'subnet-09a4d21042c23577b')
            self.assertEqual(nat_gw.eni_id, 'eni-01c1096f17feea290')
            self.assertEqual(nat_gw.private_ip, '192.168.100.153')
            self.assertEqual(nat_gw.public_ip, '18.193.200.178')
            self.assertEqual(nat_gw.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/vpc/home?region=us-east-1#NatGatewayDetails:natGatewayId=nat-0b8341023f3285b54')
