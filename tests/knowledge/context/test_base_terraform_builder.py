# pylint: disable=no-self-use
import unittest
from typing import Type

from parameterized import parameterized
from mockito import mock

from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.azure.resources_builders.terraform.azure_terraform_builder import AzureTerraformBuilder
from cloudrail.knowledge.context.gcp.resources_builders.terraform.base_gcp_terraform_builder import BaseGcpTerraformBuilder
from cloudrail.knowledge.context.base_context_builders.base_terraform_builder import BaseTerraformBuilder
from cloudrail.knowledge.context.environment_context.terraform_resource_finder import TerraformResourceFinder


class TestBaseTerraformBuilder(unittest.TestCase):

    @parameterized.expand(
        [
            ['aws', AwsTerraformBuilder],
            ['azure', AzureTerraformBuilder],
            ['gcp', BaseGcpTerraformBuilder]
        ]
    )
    def test_aws_builder_continues_on_do_build_exception(self, unused_name, builder_type: Type[BaseTerraformBuilder]):
        item = mock({'id': '1', 'iac_state': None})
        service_name = mock({'value': 'service_name'})

        class TerraformBuilderForTest(builder_type):

            def do_build(self, attributes: dict):
                if attributes['raise']:
                    raise Exception()
                return item

            def _build(self):
                attributes = self.resources[self.get_service_name().value]
                results = []
                for attribute in attributes:
                    try:
                        results.append(self.do_build(attribute))
                    except: # pylint: disable=bare-except
                        pass
                return results

            def get_service_name(self):
                return service_name

        builder = TerraformBuilderForTest({
            'service_name': [
                {
                    'raise': True,
                    'tf_action': 'read',
                    'cloudrail_resource_metadata': None
                },
                {
                    'raise': False,
                    'tf_action': 'read',
                    'cloudrail_resource_metadata': None
                }
            ]
        })
        TerraformResourceFinder.initialize()
        results = builder.build()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], item)

    @parameterized.expand(
        [
            ['aws', AwsTerraformBuilder],
            ['azure', AzureTerraformBuilder],
            ['gcp', BaseGcpTerraformBuilder]
        ]
    )
    def test_aws_builder_continues_on_build_exception(self, unused_name, builder_type: Type[BaseTerraformBuilder]):
        service_name = mock({'value': 'service_name'})

        class TerraformBuilderForTest(builder_type):

            def do_build(self, attributes: dict):
                pass

            def _build(self):
                raise Exception()

            def get_service_name(self):
                return service_name

        builder = TerraformBuilderForTest({
            'service_name': [
                {
                    'tf_action': 'read',
                    'cloudrail_resource_metadata': None
                }
            ]
        })
        TerraformResourceFinder.initialize()
        results = builder.build()
        self.assertEqual(len(results), 0)

    @parameterized.expand(
        [
            ['aws', AwsTerraformBuilder],
            ['azure', AzureTerraformBuilder],
            ['gcp', BaseGcpTerraformBuilder]
        ]
    )
    def test_aws_builder_not_failing_on_post_build_exception(self, unused_name, builder_type: Type[BaseTerraformBuilder]):
        item = mock({'id': '1', 'iac_state': None})
        service_name = mock({'value': 'service_name'})

        class TerraformBuilderForTest(builder_type):

            def do_build(self, attributes: dict):
                pass

            def _build(self):
                return [item]

            @staticmethod
            def _post_build(build_results) -> list:
                raise Exception()

            def get_service_name(self):
                return service_name

        builder = TerraformBuilderForTest({
            'service_name': [
                {
                    'tf_action': 'read',
                    'cloudrail_resource_metadata': None
                },
                {
                    'tf_action': 'read',
                    'cloudrail_resource_metadata': None
                }
            ]
        })
        TerraformResourceFinder.initialize()
        results = builder.build()
        self.assertEqual(len(results), 0)
