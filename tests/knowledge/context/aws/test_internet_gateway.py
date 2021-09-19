from cloudrail.knowledge.context.aws.resources.ec2.igw_type import IgwType
from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext
from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import TestOptions, context


class TestEgressOnlyInternetGateway(AwsContextTest):

    def get_component(self):
        return "igw"

    @context(module_path="with_public_egress_igw", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_egress_igw(self, ctx: AwsEnvironmentContext):
        vpc = next(vpc for vpc in ctx.vpcs if vpc.name == 'igw-vpc')
        igw = next(igw for igw in ctx.internet_gateways if igw.vpc_id == vpc.vpc_id)
        self.assertEqual(igw.igw_type, IgwType.EGRESS_ONLY_IGW)
        self.assertFalse(igw.tags)
        if not igw.is_managed_by_iac:
            self.assertEqual(igw.get_cloud_resource_url(),
                             'https://console.aws.amazon.com/vpc/home?region=us-east-1#InternetGateway:internetGatewayId=eigw-0ded1411d0f0a0f45')

        self.assertTrue(any(rt for rt in ctx.route_tables
                            for route in rt.routes
                            if route.target == igw.igw_id and route.destination == "::/0"),
                        "no route table contain egress only igw route")

    @context(module_path="with_tags", test_options=TestOptions(always_use_cache_on_jenkins=True))
    def test_egress_igw_with_tags(self, ctx: AwsEnvironmentContext):
        vpc = next(vpc for vpc in ctx.vpcs if vpc.name == 'igw-vpc')
        igw = next(igw for igw in ctx.internet_gateways if igw.vpc_id == vpc.vpc_id)
        self.assertIsNotNone(igw)
        self.assertTrue(igw.tags)
