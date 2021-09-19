from cloudrail.knowledge.context.aws.aws_environment_context import AwsEnvironmentContext

from tests.knowledge.context.aws_context_test import AwsContextTest
from tests.knowledge.context.test_context_annotation import context, TestOptions


class TestMultiProvider(AwsContextTest):

    def get_component(self):
        return "multi_provider"

    @context(module_path="no_provider", test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False, use_cached_plan_data_ratio=0))
    def test_no_provider(self, ctx: AwsEnvironmentContext):
        # If no provider is confiigured, will use us-east-1 as default
        vpc = next((vpc for vpc in ctx.vpcs if vpc.name == 'us-east-1'), None)
        self.assertIsNotNone(vpc)
        self.assertEqual(vpc.region, 'us-east-1')

    @context(module_path="multi_region", test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False))
    def test_multi_region(self, ctx: AwsEnvironmentContext):
        vpc_east = next((vpc for vpc in ctx.vpcs if vpc.name == 'us-east-1'), None)
        self.assertIsNotNone(vpc_east)
        vpc_west = next((vpc for vpc in ctx.vpcs if vpc.name == 'us-west-1'), None)
        self.assertIsNotNone(vpc_west)

        self.assertEqual(vpc_east.region, 'us-east-1')
        self.assertEqual(vpc_west.region, 'us-west-1')

    @context(module_path="with_a_module", test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False))
    def test_with_a_module(self, ctx: AwsEnvironmentContext):
        vpc_east = next((vpc for vpc in ctx.vpcs if vpc.name == 'east'), None)
        self.assertIsNotNone(vpc_east)
        vpc_west = next((vpc for vpc in ctx.vpcs if vpc.name == 'west'), None)
        self.assertIsNotNone(vpc_west)

        self.assertEqual(vpc_east.region, 'us-east-1')
        self.assertEqual(vpc_west.region, 'us-west-1')

    @context(module_path="with_modules", test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False))
    def test_with_modules(self, ctx: AwsEnvironmentContext):
        main_vpc_east1 = next((vpc for vpc in ctx.vpcs if vpc.name == 'east1'), None)
        self.assertIsNotNone(main_vpc_east1)
        self.assertEqual(main_vpc_east1.region, 'us-east-1')

        vpc_module_vpc_east2 = next((vpc for vpc in ctx.vpcs if vpc.name == 'vpc_module-east2'), None)
        self.assertIsNotNone(vpc_module_vpc_east2)
        self.assertEqual(vpc_module_vpc_east2.region, 'us-east-2')

        nested_vpc_module_vpc_east2 = next((vpc for vpc in ctx.vpcs if vpc.name == 'nested_vpc_module-east2'), None)
        self.assertIsNotNone(nested_vpc_module_vpc_east2)
        self.assertEqual(nested_vpc_module_vpc_east2.region, 'us-east-2')

        nested_vpc_module_vpc_west = next((vpc for vpc in ctx.vpcs if vpc.name == 'nested_vpc_module-west'), None)
        self.assertIsNotNone(nested_vpc_module_vpc_west)
        self.assertEqual(nested_vpc_module_vpc_west.region, 'us-west-1')

    @context(module_path="region_from_variable", test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False))
    def test_region_from_variable(self, ctx: AwsEnvironmentContext):
        main_vpc_west1 = next((vpc for vpc in ctx.vpcs if vpc.name == 'us-west-1'), None)
        self.assertIsNotNone(main_vpc_west1)
        self.assertEqual(main_vpc_west1.region, 'us-west-1')

    @context(module_path="region_from_module_variable", test_options=TestOptions(always_use_cache_on_jenkins=True, run_cloudmapper=False))
    def test_region_from_module_variable(self, ctx: AwsEnvironmentContext):
        vpc_east1 = next((vpc for vpc in ctx.vpcs if vpc.name == 'east'), None)
        self.assertIsNotNone(vpc_east1)
        self.assertEqual(vpc_east1.region, 'us-east-1')

        vpc_west1 = next((vpc for vpc in ctx.vpcs if vpc.name == 'west'), None)
        self.assertIsNotNone(vpc_west1)
        self.assertEqual(vpc_west1.region, 'us-west-1')

        print(f'{vpc_east1.get_friendly_name()} - us-east-1')
        print(f'{vpc_west1.get_friendly_name()} - us-west-1')
