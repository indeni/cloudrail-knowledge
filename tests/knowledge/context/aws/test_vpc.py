from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from cloudrail.knowledge.context.aws.resources.ec2.vpc import Vpc

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context


class TestVpc(AwsContextTest):

    def get_component(self):
        return "vpc"

    @context(module_path="none-default-vpc")
    def test_none_default_vpc(self, ctx: AwsEnvironmentContext):
        vpc = self._vpc_assertion(ctx, False, "none-default-vpc")
        self.assertEqual(['172.27.0.0/16'], vpc.cidr_block)
        if not vpc.is_new_resource():
            expected_cloud_resource_url = 'https://console.aws.amazon.com/vpc/home?region=us-east-1#VpcDetails:VpcId=vpc-06c90a717bf0c331f'
            self.assertEqual(expected_cloud_resource_url, vpc.get_cloud_resource_url())

    @context(module_path="default-vpc")
    def test_default_vpc(self, ctx: AwsEnvironmentContext):
        self._vpc_assertion(ctx, True, "default-vpc")

    @context(module_path="vpc-dns-resolution")
    def test_vpc_attributes(self, ctx: AwsEnvironmentContext):
        vpc = self._vpc_assertion(ctx, False, "none-default-vpc")
        self.assertTrue(vpc.enable_dns_support)
        self.assertTrue(vpc.enable_dns_hostnames)

    def _vpc_assertion(self, ctx: AwsEnvironmentContext, default_vpc: bool, vpc_name: str) -> Vpc:
        vpc: Vpc = next((vpc for vpc in ctx.vpcs if vpc.name == vpc_name), None)
        self.assertIsNotNone(vpc)
        self.assertEqual(vpc_name, vpc.name)
        self.assertTrue(vpc.region)
        self.assertTrue(vpc.account)
        self.assertEqual(default_vpc, vpc.is_default)
        self.assertIsNotNone(vpc.main_route_table)
        self.assertEqual(vpc_name, vpc.tags['Name'])
        return vpc

    @context(module_path="with_public_reg_igw")
    def test_with_public_reg_igw(self, ctx: AwsEnvironmentContext):
        vpc = self._vpc_assertion(ctx, False, "external-vpc")
        self.assertIsNotNone(vpc)
        self.assertTrue(vpc.internet_gateway)

    @context(module_path="vpc_with_ipv6_and_nacl")
    def test_vpc_with_ipv6_and_nacl(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.cidr_block == ['192.168.10.0/24']), None)
        self.assertIsNotNone(vpc)
        self.assertTrue(vpc.ipv6_cidr_block)
        if vpc.is_managed_by_iac:
            self.assertEqual(vpc.ipv6_cidr_block, ['aws_vpc.test-vpc.ipv6_cidr_block'])
        else:
            self.assertEqual(vpc.ipv6_cidr_block, ['2600:1f18:6407:5200::/56'])

    @context(module_path="vpc_with_ipv6_default_nacl")
    def test_vpc_with_ipv6_default_nacl(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.cidr_block == ['192.168.10.0/24']), None)
        self.assertIsNotNone(vpc)
        self.assertTrue(vpc.ipv6_cidr_block)
        if vpc.is_managed_by_iac:
            self.assertEqual(vpc.ipv6_cidr_block, ['aws_vpc.test-vpc.ipv6_cidr_block'])
        else:
            self.assertEqual(vpc.ipv6_cidr_block, ['2600:1f18:2212:5300::/56'])

    @context(module_path="default_vpc_ipv6_enabled_with_nacl")
    def test_default_vpc_ipv6_enabled_with_nacl(self, ctx: AwsEnvironmentContext):
        vpc = next((vpc for vpc in ctx.vpcs if vpc.cidr_block == ['172.31.0.0/16']), None)
        self.assertIsNotNone(vpc)
        if vpc.ipv6_cidr_block:
            self.assertEqual(vpc.ipv6_cidr_block, ['2600:1f18:2578:6b00::/56'])
